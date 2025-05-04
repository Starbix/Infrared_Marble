import datetime
from lib.utils import LJ_DATA_DIR, DATA_DIR

from shapely.geometry import Polygon
import geopandas
import xarray
from osgeo import gdal, ogr
from pathlib import Path
from geopandas import GeoDataFrame

DEBUG = False

def get_geotiffs(gdf: "GeoDataFrame", date_range: datetime.date | list[datetime.date]) -> list:
    """
    Get the list of geotiffs from the given GeoDataFrame and date range.
    """
    # assume metadata is downloaded in DATA_DIR / "luojia" / "metadata"
    relevant_geotiffs = []
    geotiff_metadata = LJ_DATA_DIR / "metadata"

    # iterate through the geotiffs and check if they are in the date and location range
    for geotiff in geotiff_metadata.glob("*.xml"):
        # parse XML file
        import xml
        from xml.etree import ElementTree
        tree = ElementTree.parse(geotiff)
        # path to Metadata.ProductInfo.imagingTime
        imaging_time = tree.find(".//imagingTime").text
        if imaging_time is None:
            if DEBUG:
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
        
        # check if the polygon intersects with the GeoDataFrame
        lt = (tree.find(".//LTLongitude").text, tree.find(".//LTLatitude").text)
        rt = (tree.find(".//RTLongitude").text, tree.find(".//RTLatitude").text)
        rb = (tree.find(".//RBLongitude").text, tree.find(".//RBLatitude").text)
        lb = (tree.find(".//LBLongitude").text, tree.find(".//LBLatitude").text)
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
    file_path = str(LJ_DATA_DIR / "tiles" / geotiff)+"_gec.tif"
    # open the geotiff
    #import geotiff

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
    ds = xarray.open_dataset(str(LJ_DATA_DIR / geotiff), decode_times=False, chunks="auto")
    # add the georeference information
    ds.rio.write_crs("epsg:4326", inplace=True)
    return ds

def downsample_xarray(ds: xarray.Dataset, factor: int = 2) -> xarray.Dataset:
    """
    Downsample the xarray dataset by a factor.
    """
    # downsample the xarray dataset
    ds = ds.coarsen(x=factor, y=factor, boundary="pad").mean()

    return ds


## problematic: noData from geotiffs overwrite actual data
# need to take geometry into account
def merge_geotiffs(geotiff_list, output_name="merged.tif"):
    file_list = [ str(LJ_DATA_DIR / "tiles" / geotiff)+"_gec.tif" for geotiff in geotiff_list]

    for file in file_list:
        metadata_path = str(LJ_DATA_DIR / "metadata" / file.split("/")[-1].replace("_gec.tif", "_meta.xml"))
        convert_geotiff(file, file.replace(".tif", "_float.tif"), metadata_path)

    new_file_list = [ str(LJ_DATA_DIR / "tiles" / geotiff)+"_gec_float.tif" for geotiff in geotiff_list]

    output_file = LJ_DATA_DIR / output_name

    vrt_options = gdal.BuildVRTOptions(srcNodata=-1)
    vrt_dataset = gdal.BuildVRT('', new_file_list, options=vrt_options)

    # Translate VRT to TIFF
    gdal.Translate(output_file, vrt_dataset, noData=-1)

    # Close the in-memory VRT dataset
    vrt_dataset = None

# convert uint32 to float32, 
def convert_geotiff(input_path, output_path, metadata_path, nodata_value=-1):
    # Open the input GeoTIFF file
    dataset = gdal.Open(input_path)
    geotransform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()
    band = dataset.GetRasterBand(1)

    # Read the data as a numpy array
    data = band.ReadAsArray()

    # Apply the radiance conversion formula
    radiance = (data ** (3/2)) * 10 ** (-10)

    driver = gdal.GetDriverByName('GTiff')
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
        "LT": (float(tree.find(".//LTLongitude").text), float(tree.find(".//LTLatitude").text)),
        "RT": (float(tree.find(".//RTLongitude").text), float(tree.find(".//RTLatitude").text)),
        "RB": (float(tree.find(".//RBLongitude").text), float(tree.find(".//RBLatitude").text)),
        "LB": (float(tree.find(".//LBLongitude").text), float(tree.find(".//LBLatitude").text)),
    }

    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(coordinates['LT'][0], coordinates['LT'][1])
    ring.AddPoint(coordinates['RT'][0], coordinates['RT'][1])
    ring.AddPoint(coordinates['RB'][0], coordinates['RB'][1])
    ring.AddPoint(coordinates['LB'][0], coordinates['LB'][1])
    ring.AddPoint(coordinates['LT'][0], coordinates['LT'][1])  # Close the ring

    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ring)

    # Create a memory layer to hold the polygon
    mem_driver = ogr.GetDriverByName('MEMORY')
    mem_source = mem_driver.CreateDataSource('memData')
    mem_layer = mem_source.CreateLayer('memLayer', srs=ogr.osr.SpatialReference(wkt=projection))
    feature = ogr.Feature(mem_layer.GetLayerDefn())
    feature.SetGeometry(polygon)
    mem_layer.CreateFeature(feature)

    # Rasterize the polygon to create a mask
    driver = gdal.GetDriverByName('MEM')
    mask_dataset = driver.Create('', dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Byte)
    mask_dataset.SetGeoTransform(geotransform)
    mask_dataset.SetProjection(projection)
    gdal.RasterizeLayer(mask_dataset, [1], mem_layer, burn_values=[1])
    mask = mask_dataset.GetRasterBand(1).ReadAsArray()

    # Apply the mask to set values outside the mask to 1
    radiance[mask == 0] = nodata_value

    # Create a new GeoTIFF file to save the result
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(output_path, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Float32)
    out_dataset.SetGeoTransform(geotransform)
    out_dataset.SetProjection(projection)
    out_band = out_dataset.GetRasterBand(1)
    out_band.WriteArray(radiance)
    out_band.FlushCache()
    # Close the datasets
    dataset = None
    out_dataset = None


def visualize_geotiff(file: str):
    """
    Visualize the geotiff using matplotlib.
    """
    import geotiff
    geo_tiff = geotiff.GeoTiff(file)
    # get the data
    print(geo_tiff)
    print(geo_tiff.tif_shape)
    print(geo_tiff.tif_bBox)

    zarr_array = geo_tiff.read()
    import numpy as np

    array = np.array(zarr_array)


if __name__ == "__main__":
    # visualize_geotiff("/Users/cedriclaubacher/ETH/Infrared_Marble/data/luojia/tiles/LuoJia1-01_LR201811208517_20181119160335_HDR_0024_gec.tif")
    # pass
    #exit(0)
    GDF_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_MMR_1.json.zip"
    GDF_DOWNLOAD_PATH = DATA_DIR / Path(GDF_URL).name

    gdf = geopandas.read_file(GDF_DOWNLOAD_PATH)
    date = datetime.date(2018, 11, 2)
    # Generate a list of dates for November 2018 and 2019
    date_list = [
        datetime.date(year, 11, day)
        for year in [2018, 2019]
        for day in range(1, 31 )  # Days in November
    ]

    geotiff_list = get_geotiffs(gdf, date)

    # download geotiffs
    from lib.download import luojia_tile_download
    for geotiff in geotiff_list:
        luojia_tile_download(geotiff)
    
    # merge geotiffs
    merge_geotiffs(geotiff_list)

    # get xarray
    ds = get_xarray_from_geotiff("merged.tif")
    # print the xarray

    ds = downsample_xarray(ds, factor=10)
    # print the xarray

    import matplotlib.pyplot as plt
    import colorcet as cc
    import contextily as cx

    def plot_day():
        fig, ax = plt.subplots(figsize=(8, 14))

        ds["band_data"].sel(
            band=1
        ).plot.pcolormesh(
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
        #plt.savefig("output.pdf", bbox_inches="tight", dpi=300)
        plt.show()

    plot_day()
