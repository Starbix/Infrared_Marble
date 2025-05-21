import gzip
from pathlib import Path

import geopandas
import pandas as pd

from lib.config import ADMIN_AREA_FILE_MAPPING, DEFAULT_DATES_FILE, GEOJSON_ADMIN_KEY, STATIC_DIR, TILE_DENSITY_CSV
from lib.app_types import Resolution


def dates_from_csv(filename: str | Path | None = None, colname: str = "date") -> list[str]:
    """Returns a list of dates from a CSV file.

    :param file: Path to file to load. Can be either a local file or remote URL. Defaults to DEFAULT_DATES_FILE
    :param colname: Column name for the dates column, defaults to "date"
    :return: List of date strings in ISO format, sorted in ascending order
    """
    df = pd.read_csv(filename or DEFAULT_DATES_FILE)
    date_list = df[colname].dropna().sort_values().unique().tolist()
    return date_list


def get_all_regions_gdf(resolution: Resolution = "50m") -> geopandas.GeoDataFrame:
    """Get a GeoDataFrame from a pre-defined GeoJSON file at a configurable resolution for all available regions.

    :param resolution: Geometry resolution, defaults to "50m"
    :return: GeoDataFrame
    """
    with gzip.open(ADMIN_AREA_FILE_MAPPING[resolution]) as f:
        return geopandas.read_file(f)


def get_region_avail_dates(admin_id: str) -> list[str]:
    """Gets a list of available dates for a given region

    :param admin_id: Administrative ID of the region of interest
    :return: List of dates (string), in ISO format, sorted in ascending order
    """
    country_meta = pd.read_csv(STATIC_DIR / "country_meta.csv.gz")
    dates = country_meta[country_meta["country"] == admin_id]["date"]
    dates = dates.sort_values().unique()
    return dates.tolist()


def get_region_gdf(admin_id: str) -> geopandas.GeoDataFrame:
    """Get a GeoDataFrame for a particular region.

    :param admin_id: Administrative ID for this region.
    :return: GeoDataFrame of region
    """
    with gzip.open(ADMIN_AREA_FILE_MAPPING["50m"]) as f:
        gdf = geopandas.read_file(f)
    gdf = gdf[gdf[GEOJSON_ADMIN_KEY] == admin_id]
    assert isinstance(gdf, geopandas.GeoDataFrame)
    return gdf


def get_region_meta(path: str | Path | None = None):
    """Get a dataframe of metadata about regions and LuoJia tiles. The resulting dataframe has the following columns:

    - `country`:   Alpha-3 Admin 0 country code of region
    - `date`:      ISO date of tile
    - `tile_name`: Name of the LuoJia tile

    :param path: Path to file, if None uses default path.
    :return: DataFrame with meta information
    """
    path = Path(path) if path else STATIC_DIR / "country_meta.csv.gz"
    return pd.read_csv(path, compression="infer")


def get_tile_densities():
    """Get a dataframe containing information about tile density for each region

    :return: DataFrame with columns:

        - `Date` (str): Date of tile
        - `ISO_A3` (str): ISO-Alpha3 name of country
        - `Country` (str): Full name of country
        - `Count` (int): Number of tiles on this date
        - `Area_km2` (float): Country area in km^2
        - `CoverageFraction` (float): Fraction of country covered on this date
    """
    return pd.read_csv(TILE_DENSITY_CSV)
