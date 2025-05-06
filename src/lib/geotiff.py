import datetime
import io
from pathlib import Path

import geopandas
import numpy as np
import rioxarray
import xarray as xr
from osgeo import gdal, ogr
from rasterio.io import MemoryFile
from rasterio.warp import Resampling
from shapely.geometry import Polygon

from lib.download import LJ_METADATA_URL, luojia_metadata
from lib.utils import DATA_DIR, LJ_DATA_DIR

DEBUG = False
NODATA_VALUE = "nan"
from geopandas import GeoDataFrame


def get_geotiffs(gdf: "GeoDataFrame", date_range: datetime.date | list[datetime.date]) -> list:
    """
    Get the list of geotiffs from the given GeoDataFrame and date range.
    """
    # assume metadata is downloaded in DATA_DIR / "luojia" / "metadata"
    relevant_geotiffs = []
    geotiff_metadata = LJ_DATA_DIR / "metadata"

    # ensure metadata is downloaded
    if not geotiff_metadata.exists():
        luojia_metadata(LJ_METADATA_URL)

    # iterate through the geotiffs and check if they are in the date and location range
    for geotiff in geotiff_metadata.glob("*.xml"):
        # parse XML file
        from xml.etree import ElementTree

        tree = ElementTree.parse(geotiff)
        # path to Metadata.ProductInfo.imagingTime
        imaging_time = tree.findtext(".//imagingTime")
        if imaging_time is None:
            print(f"imagingTime not found in {geotiff}")
            continue

        # convert to datetime, format is 2018-6-3T5:50:57.157223
        imaging_time = datetime.datetime.strptime(imaging_time, "%Y-%m-%dT%H:%M:%S.%f")
        # check if the imaging time is in the date range
        if isinstance(date_range, datetime.date):
            if imaging_time.date() != date_range:
                continue
        elif isinstance(date_range, list):
            if imaging_time.date() not in date_range:
                continue

        lt = (tree.findtext(".//LTLongitude"), tree.findtext(".//LTLatitude"))
        rt = (tree.findtext(".//RTLongitude"), tree.findtext(".//RTLatitude"))
        rb = (tree.findtext(".//RBLongitude"), tree.findtext(".//RBLatitude"))
        lb = (tree.findtext(".//LBLongitude"), tree.findtext(".//LBLatitude"))
        # check if the coordinates are valid
        if lt is None or rt is None or rb is None or lb is None:
            print(f"Coordinates not found in {geotiff}")
            continue
        geotiff_polygon = Polygon(
            [
                (float(lt[0]), float(lt[1])),
                (float(rt[0]), float(rt[1])),
                (float(rb[0]), float(rb[1])),
                (float(lb[0]), float(lb[1])),
            ]
        )
        intersects = get_intersection(gdf, geotiff_polygon)
        if intersects:
            geotiff_name = geotiff.name
            # remove _meta.xml
            geotiff_name = geotiff_name.replace("_meta.xml", "")
            relevant_geotiffs.append(geotiff_name)

    return relevant_geotiffs


def print_geotiff_metadata(geotiff: str):
    """
    Print the metadata of the geotiff.
    """
    file_path = str(LJ_DATA_DIR / "tiles" / geotiff) + "_gec.tif"
    # open the geotiff
    # import geotiff

    ds = gdal.Open(file_path)
    # get the metadata
    metadata = ds.GetMetadata()
    # get the projection
    projection = ds.GetProjection()
    # get the geotransform
    geotransform = ds.GetGeoTransform()
    # get the band
    band = ds.GetRasterBand(1)
    # get the nodata value
    nodata_value = band.GetNoDataValue()
    # get the min and max values
    min_value = band.GetMinimum()
    max_value = band.GetMaximum()

    print(f"Metadata for {geotiff}:")
    print(f"Projection: {projection}")
    print(f"Metadata: {metadata}")


def get_intersection(gdf: "GeoDataFrame", geotiff_polygon: Polygon) -> bool:
    # Create a GeoSeries from the polygon
    geotiff_geoseries = geopandas.GeoSeries([geotiff_polygon], crs=gdf.crs)

    # Check for intersection
    intersection = gdf.intersects(geotiff_geoseries.union_all())
    return intersection.any()


def get_xarray_from_geotiff(geotiff: str):
    """
    Get the xarray from the geotiff.
    """
    # open the geotiff
    ds = xr.open_dataset(str(LJ_DATA_DIR / geotiff), decode_times=False, chunks="auto")
    # add the georeference information
    ds.rio.write_crs("epsg:4326", inplace=True)
    return ds


def downsample_xarray(ds: xr.Dataset, factor: int = 2) -> xr.Dataset:
    """
    Downsample the xarray dataset by a factor.
    """
    # downsample the xarray dataset
    ds = ds.coarsen(x=factor, y=factor, boundary="pad").mean()

    return ds


def empty_geotiff() -> bytes:
    """
    Create a minimal empty GeoTIFF with NaN as the no-data value and return it as bytes.

    Returns:
    - bytes: The GeoTIFF file as bytes.
    """
    # Create an in-memory file for the GeoTIFF
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create("/vsimem/temp.tif", 1, 1, 1, gdal.GDT_Float32)

    # Set the no-data value to NaN
    band = dataset.GetRasterBand(1)
    band.SetNoDataValue(np.nan)

    # Write NaN to the single pixel
    band.WriteArray(np.array([[np.nan]]))

    # Flush data to the virtual file system
    dataset.FlushCache()

    # Read the dataset into a bytes object
    vsi_file = gdal.VSIFOpenL("/vsimem/temp.tif", "rb")
    gdal.VSIFSeekL(vsi_file, 0, 2)  # Seek to the end
    size = gdal.VSIFTellL(vsi_file)  # Get the size of the file
    gdal.VSIFSeekL(vsi_file, 0, 0)  # Seek to the beginning

    bytes_io = io.BytesIO()
    buffer = bytearray(size)
    gdal.VSIFReadL(size, size, vsi_file)
    bytes_io.seek(0)

    # Clean up
    gdal.VSIFCloseL(vsi_file)
    dataset = None
    gdal.Unlink("/vsimem/temp.tif")

    return bytes_io.getvalue()


## problematic: noData from geotiffs overwrite actual data
# need to take geometry into account
def merge_geotiffs(geotiff_list) -> tuple[bytes, float, float]:
    if geotiff_list is None or len(geotiff_list) == 0:
        print("No geotiffs found, serving empty file")
        return empty_geotiff(), 0, 0

    file_list = [str(LJ_DATA_DIR / "tiles" / geotiff) + "_gec.tif" for geotiff in geotiff_list]

    for file in file_list:
        metadata_path = str(LJ_DATA_DIR / "metadata" / file.split("/")[-1].replace("_gec.tif", "_meta.xml"))
        convert_geotiff(file, file.replace(".tif", "_float.tif"), metadata_path)

    new_file_list = [str(LJ_DATA_DIR / "tiles" / geotiff) + "_gec_float.tif" for geotiff in geotiff_list]

    vrt_options = gdal.BuildVRTOptions(srcNodata=NODATA_VALUE)
    vrt_dataset = gdal.BuildVRT("", new_file_list, options=vrt_options)

    # Create an in-memory buffer to hold the GeoTIFF data
    mem_driver = gdal.GetDriverByName("MEM")
    mem_dataset = mem_driver.CreateCopy("", vrt_dataset, 0)

    compression_options = [
        "COMPRESS=LZW"  # You can use other compression methods like 'DEFLATE' or 'JPEG'
    ]

    # Serialize the in-memory dataset to a byte buffer
    buffer = io.BytesIO()
    gdal.Translate(
        "/vsimem/temp.tif", mem_dataset, format="GTiff", creationOptions=compression_options, noData=NODATA_VALUE
    )

    # Open the virtual file and read its content into the buffer
    vsi_file = gdal.VSIFOpenL("/vsimem/temp.tif", "rb")
    gdal.VSIFSeekL(vsi_file, 0, 2)  # Seek to the end of the file
    file_size = gdal.VSIFTellL(vsi_file)  # Get the file size
    gdal.VSIFSeekL(vsi_file, 0, 0)  # Seek back to the beginning
    buffer.write(gdal.VSIFReadL(1, file_size, vsi_file))
    buffer.seek(0)

    data_array = mem_dataset.GetRasterBand(1).ReadAsArray()

    # Calculate the 2nd and 98th percentiles, ignoring NaN values
    pc02 = np.nanpercentile(data_array, 2)
    pc98 = np.nanpercentile(data_array, 98)

    # Close the datasets
    vrt_dataset = None
    mem_dataset = None

    # Clean up the virtual file system
    gdal.Unlink("/vsimem/temp.tif")

    return buffer.read(), pc02, pc98


def resample_geotiff(input_buf: bytes, resolution: tuple[float, float] = (750.0, 750.0)) -> bytes:
    with MemoryFile(input_buf) as memfile:
        with memfile.open() as src:
            da = rioxarray.open_rasterio(src)
            assert isinstance(da, xr.DataArray), "Got more than one variable"

    resampled_da = da.rio.reproject(da.rio.crs, resolution=resolution, resampling=Resampling.bilinear)

    # Output to geotiff again
    with io.BytesIO() as output_buf:
        resampled_da.rio.to_raster(
            output_buf,
            driver="GTiff",
            compress="LZW",
            tiled=True,
            blockxsize=256,
            blockysize=256,
            windowed=True,
        )
        output_buf.seek(0)
        resampled_bytes = output_buf.getvalue()

    return resampled_bytes


def merge_geotiffs_to_file(geotiff_list, output_name="merged.tif"):
    file_list = [str(LJ_DATA_DIR / "tiles" / geotiff) + "_gec.tif" for geotiff in geotiff_list]

    for file in file_list:
        metadata_path = str(LJ_DATA_DIR / "metadata" / file.split("/")[-1].replace("_gec.tif", "_meta.xml"))
        convert_geotiff(file, file.replace(".tif", "_float.tif"), metadata_path)

    new_file_list = [str(LJ_DATA_DIR / "tiles" / geotiff) + "_gec_float.tif" for geotiff in geotiff_list]

    output_file = LJ_DATA_DIR / output_name

    vrt_options = gdal.BuildVRTOptions(srcNodata=NODATA_VALUE)
    vrt_dataset = gdal.BuildVRT("", new_file_list, options=vrt_options)

    # Translate VRT to TIFF
    gdal.Translate(output_file, vrt_dataset, noData=NODATA_VALUE)

    # Close the in-memory VRT dataset
    vrt_dataset = None


# convert uint32 to float32,
def convert_geotiff(input_path, output_path, metadata_path, nodata_value=NODATA_VALUE):
    # Open the input GeoTIFF file
    dataset = gdal.Open(input_path)
    geotransform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()
    band = dataset.GetRasterBand(1)

    # Read the data as a numpy array
    data = band.ReadAsArray()

    # Apply the radiance conversion formula
    radiance = (data ** (3 / 2)) * 10 ** (-10)

    driver = gdal.GetDriverByName("GTiff")
    out_dataset = driver.Create(output_path, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Float32)
    out_dataset.SetGeoTransform(dataset.GetGeoTransform())
    out_dataset.SetProjection(dataset.GetProjection())
    out_band = out_dataset.GetRasterBand(1)
    out_band.WriteArray(radiance)
    out_band.FlushCache()

    # read metadata from the XML file
    from xml.etree import ElementTree

    tree = ElementTree.parse(metadata_path)
    coordinates = {
        "LT": (float(tree.findtext(".//LTLongitude") or 0.0), float(tree.findtext(".//LTLatitude") or 0.0)),
        "RT": (float(tree.findtext(".//RTLongitude") or 0.0), float(tree.findtext(".//RTLatitude") or 0.0)),
        "RB": (float(tree.findtext(".//RBLongitude") or 0.0), float(tree.findtext(".//RBLatitude") or 0.0)),
        "LB": (float(tree.findtext(".//LBLongitude") or 0.0), float(tree.findtext(".//LBLatitude") or 0.0)),
    }

    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(coordinates["LT"][0], coordinates["LT"][1])
    ring.AddPoint(coordinates["RT"][0], coordinates["RT"][1])
    ring.AddPoint(coordinates["RB"][0], coordinates["RB"][1])
    ring.AddPoint(coordinates["LB"][0], coordinates["LB"][1])
    ring.AddPoint(coordinates["LT"][0], coordinates["LT"][1])  # Close the ring

    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ring)

    # Create a memory layer to hold the polygon
    mem_driver = ogr.GetDriverByName("MEMORY")
    mem_source = mem_driver.CreateDataSource("memData")
    mem_layer = mem_source.CreateLayer("memLayer", srs=ogr.osr.SpatialReference(wkt=projection))
    feature = ogr.Feature(mem_layer.GetLayerDefn())
    feature.SetGeometry(polygon)
    mem_layer.CreateFeature(feature)

    # Rasterize the polygon to create a mask
    driver = gdal.GetDriverByName("MEM")
    mask_dataset = driver.Create("", dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Byte)
    mask_dataset.SetGeoTransform(geotransform)
    mask_dataset.SetProjection(projection)
    gdal.RasterizeLayer(mask_dataset, [1], mem_layer, burn_values=[1])
    mask = mask_dataset.GetRasterBand(1).ReadAsArray()

    # Apply the mask to set values outside the mask to 1
    radiance[mask == 0] = nodata_value

    # Create a new GeoTIFF file to save the result
    driver = gdal.GetDriverByName("GTiff")
    out_dataset = driver.Create(output_path, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Float32)
    out_dataset.SetGeoTransform(geotransform)
    out_dataset.SetProjection(projection)
    out_band = out_dataset.GetRasterBand(1)
    out_band.WriteArray(radiance)
    out_band.FlushCache()
    # Close the datasets
    dataset = None
    out_dataset = None


if __name__ == "__main__":
    # visualize_geotiff("/Users/cedriclaubacher/ETH/Infrared_Marble/data/luojia/tiles/LuoJia1-01_LR201811208517_20181119160335_HDR_0024_gec.tif")
    # pass
    # exit(0)
    GDF_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_MMR_1.json.zip"
    GDF_DOWNLOAD_PATH = DATA_DIR / Path(GDF_URL).name

    gdf = geopandas.read_file(GDF_DOWNLOAD_PATH)
    date = datetime.date(2018, 11, 2)
    # Generate a list of dates for November 2018 and 2019
    date_list = [
        datetime.date(year, 11, day)
        for year in [2018, 2019]
        for day in range(1, 31)  # Days in November
    ]

    geotiff_list = get_geotiffs(gdf, date)

    # download geotiffs
    from lib.download import luojia_tile_download

    for geotiff in geotiff_list:
        luojia_tile_download(geotiff)

    # merge geotiffs
    geotiff, pc02, pc98 = merge_geotiffs(geotiff_list)

    # get xarray
    ds = get_xarray_from_geotiff("merged.tif")
    # print the xarray

    ds = downsample_xarray(ds, factor=10)
    # print the xarray

    import colorcet as cc
    import contextily as cx
    import matplotlib.pyplot as plt

    def plot_day():
        fig, ax = plt.subplots(figsize=(8, 14))

        ds["band_data"].sel(band=1).plot.pcolormesh(
            ax=ax,
            cmap=cc.cm.bmy,
            robust=True,
        )
        assert gdf.crs is not None
        cx.add_basemap(ax, crs=gdf.crs.to_string())

        ax.text(
            0,
            -0.1,
            "Source: NASA Black Marble VNP46A2",
            ha="left",
            va="center",
            transform=ax.transAxes,
            fontsize=10,
            color="black",
            weight="normal",
        )
        ax.set_title("Myanmar: NTL Radiance on Mar 27, 2019", fontsize=20)

        # save pdf
        # plt.savefig("output.pdf", bbox_inches="tight", dpi=300)
        plt.show()

    plot_day()
