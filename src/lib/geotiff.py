import datetime
from typing import TYPE_CHECKING
from lib.utils import LJ_DATA_DIR

from shapely.geometry import Polygon
import geopandas
import xarray
from osgeo import gdal

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

    return relevant_geotiffs


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
    output_file = LJ_DATA_DIR / output_name
    vrt_file = "merged.vrt"
    gdal.BuildVRT(vrt_file,file_list,
                  )

    # Translate VRT to TIFF
    gdal.Translate(output_file,vrt_file,
                   noData="0")


# if __name__ == "__main__":
#     GDF_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_MMR_1.json.zip"
#     GDF_DOWNLOAD_PATH = DATA_DIR / Path(GDF_URL).name

#     gdf = geopandas.read_file(GDF_DOWNLOAD_PATH)
#     date = datetime.date(2018, 11, 2)
#     # Generate a list of dates for November 2018 and 2019
#     date_list = [
#         datetime.date(year, 11, day)
#         for year in [2018, 2019]
#         for day in range(1, 31 )  # Days in November
#     ]


#     geotiff_list = get_geotiffs(gdf, date_list)
#     print(geotiff_list)

#     # download geotiffs
#     from lib.download import luojia_tile_download
#     for geotiff in geotiff_list:
#         luojia_tile_download(geotiff)
    
#     # merge geotiffs
#     merge_geotiffs(geotiff_list)

#     # get xarray
#     ds = get_xarray_from_geotiff("merged.tif")
#     # print the xarray
#     print(ds)

#     ds = downsample_xarray(ds, factor=10)
#     # print the xarray
#     print(ds)

#     import matplotlib.pyplot as plt
#     import colorcet as cc
#     import contextily as cx

#     def plot_day():
#         fig, ax = plt.subplots(figsize=(8, 14))

#         ds["band_data"].sel(
#             band=1
#         ).plot.pcolormesh(
#             ax=ax,
#             cmap=cc.cm.bmy,
#             robust=True,
#         )
#         assert gdf.crs is not None
#         cx.add_basemap(ax, crs=gdf.crs.to_string())

#         ax.text(
#             0,
#             -0.1,
#             "Source: NASA Black Marble VNP46A2",
#             ha="left",
#             va="center",
#             transform=ax.transAxes,
#             fontsize=10,
#             color="black",
#             weight="normal",
#         )
#         ax.set_title("Myanmar: NTL Radiance on Mar 27, 2019", fontsize=20)

#         # save pdf
#         #plt.savefig("output.pdf", bbox_inches="tight", dpi=300)
#         plt.show()

#     plot_day()
