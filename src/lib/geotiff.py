import datetime
from typing import TYPE_CHECKING
from lib.utils import LJ_DATA_DIR, DATA_DIR

from shapely.geometry import Polygon
import geopandas
import xarray
from osgeo import gdal
from pathlib import Path
import numpy as np

if TYPE_CHECKING:
    from geopandas import GeoDataFrame

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
        # convert to datetime, format is 2018-6-3T5:50:57.157223
        imaging_time = datetime.datetime.strptime(imaging_time, "%Y-%m-%dT%H:%M:%S.%f")
        # check if the imaging time is in the date range
        if isinstance(date_range, datetime.date):
            if imaging_time.date() != date_range:
                continue
        elif isinstance(date_range, list):
            if imaging_time.date() not in date_range:
                continue
        

        # <LTLongitude>-115.888656</LTLongitude>
        # <LTLatitude>35.301386</LTLatitude>
        # <RTLongitude>-115.211464</RTLongitude>
        # <RTLatitude>33.013016</RTLatitude>
        # <RBLongitude>-118.077200</RBLongitude>
        # <RBLatitude>32.341746</RBLatitude>
        # <LBLongitude>-118.911156</LBLongitude>
        # <LBLatitude>34.815542</LBLatitude>
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
        # check if the polygon intersects with the GeoDataFrame
        intersects = get_intersection(gdf, geotiff_polygon)
        if intersects:
            geotiff_name = geotiff.name
            # remove _meta.xml
            geotiff_name = geotiff_name.replace("_meta.xml", "")
            relevant_geotiffs.append(geotiff_name)
            print_geotiff_metadata(geotiff_name)


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
        convert_geotiff(file, file.replace(".tif", "_float.tif"))

    new_file_list = [ str(LJ_DATA_DIR / "tiles" / geotiff)+"_gec.tif" for geotiff in geotiff_list]

    output_file = LJ_DATA_DIR / output_name
    vrt_file = "merged.vrt"
    gdal.BuildVRT(vrt_file,new_file_list,
                  )

    # Translate VRT to TIFF
    gdal.Translate(output_file,vrt_file,
                   noData="0")

# convert uint32 to float32, 
def convert_geotiff(input_path, output_path, nodata_value=-9999):
    # Open the input GeoTIFF file
    dataset = gdal.Open(input_path)
    band = dataset.GetRasterBand(1)

    # Read the data as a numpy array
    data = band.ReadAsArray()

    # Apply the radiance conversion formula
    radiance = (data**(3/2)) / (10**10)

    # Set NODATA value for out-of-bounds data


 # Get the geotransform
    geotransform = dataset.GetGeoTransform()
    min_x = geotransform[0]
    max_y = geotransform[3]
    pixel_size_x = geotransform[1]
    pixel_size_y = geotransform[5]

    # Calculate the coordinates for each pixel
    x_coords = np.arange(min_x, min_x + dataset.RasterXSize * pixel_size_x, pixel_size_x)[:dataset.RasterXSize]
    y_coords = np.arange(max_y, max_y + dataset.RasterYSize * pixel_size_y, pixel_size_y)[:dataset.RasterYSize]
    xx, yy = np.meshgrid(x_coords, y_coords)

    # Define the corner coordinates
    corner_coords = {
        'min_x': min_x,
        'max_x': min_x + dataset.RasterXSize * pixel_size_x,
        'min_y': max_y + dataset.RasterYSize * pixel_size_y,
        'max_y': max_y
    }

    # Create a mask for the valid data region
    valid_mask = (xx >= corner_coords['min_x']) & (xx < corner_coords['max_x']) & (yy >= corner_coords['min_y']) & (yy < corner_coords['max_y'])

    # Apply the mask to set NODATA values
    radiance[~valid_mask] = nodata_value
    # Create a new GeoTIFF file
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(output_path, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Float32)

    # Copy the geotransform and projection
    out_dataset.SetGeoTransform(dataset.GetGeoTransform())
    out_dataset.SetProjection(dataset.GetProjection())

    # Copy metadata
    out_dataset.SetMetadata(dataset.GetMetadata())

    # Write the radiance data to the new file
    out_band = out_dataset.GetRasterBand(1)
    out_band.WriteArray(radiance)
    out_band.SetNoDataValue(nodata_value)  # Set NODATA value in metadata
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
    print(GDF_DOWNLOAD_PATH)

    gdf = geopandas.read_file(GDF_DOWNLOAD_PATH)
    date = datetime.date(2018, 11, 2)
    # Generate a list of dates for November 2018 and 2019
    date_list = [
        datetime.date(year, 11, day)
        for year in [2018, 2019]
        for day in range(1, 31 )  # Days in November
    ]


    geotiff_list = get_geotiffs(gdf, date)
    print(geotiff_list)

    # download geotiffs
    from lib.download import luojia_tile_download
    for geotiff in geotiff_list:
        luojia_tile_download(geotiff)
    
    # merge geotiffs
    merge_geotiffs(geotiff_list)

    # get xarray
    ds = get_xarray_from_geotiff("merged.tif")
    # print the xarray
    print(ds)


    ds = downsample_xarray(ds, factor=10)
    # print the xarray
    print(ds)

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
