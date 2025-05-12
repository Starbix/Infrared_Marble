import datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import xarray as xr
from blackmarble.raster import bm_raster
from geopandas import GeoDataFrame

from lib.config import (
    BM_DATA_DIR,
    BM_PRODUCT,
    BM_QUALITY_FLAG,
    BM_TOKEN,
    BM_VARIABLE,
)


def bm_download(gdf: "GeoDataFrame", date_range: datetime.date | list[datetime.date]) -> xr.Dataset:
    """Downloads data from Blackmarble dataset for a given region and date range.

    :param gdf: GeoDataFrame of region of interest
    :param date_range: Single date or list of dates to download data for
    :return: xarray.Dataset containing raster data
    """
    out_dir = BM_DATA_DIR / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    raster = bm_raster(
        gdf,
        product_id=BM_PRODUCT,
        date_range=date_range,
        bearer=BM_TOKEN,
        output_directory=out_dir,
        drop_values_by_quality_flag=BM_QUALITY_FLAG,
        variable=BM_VARIABLE,
        output_skip_if_exists=True,
    )
    return raster


def bm_store_to_zarr(
    gdf: "GeoDataFrame",
    dates: list[datetime.date],
    dest: str | Path | None = None,
    force: bool = False,
) -> xr.Dataset:
    """Downloads Blackmarble data and stores it to a Zarr backend.

    :param gdf: GeoDataFrame of region of interest
    :param dates: List of dates to download
    :param dest: Path to Zarr store, defaults to None
    :param force: Force re-downloading all files, defaults to False
    :return: Fresh reference to Zarr store
    """
    # Check if already preprocessed
    zarr_path = Path(dest) if dest else (BM_DATA_DIR / "preprocessed" / f"{BM_PRODUCT}-{BM_VARIABLE}.zarr")
    zarr_path.parent.mkdir(parents=True, exist_ok=True)
    if not force and zarr_path.exists():
        print("Dataset already preprocessed, skipping...")
        return bm_load_from_zarr(zarr_path)

    # Download all datasets for each date in parallel
    # Note: date_range does not download for each date individually, but for each date between any
    # dates in the list of dates! We need to download each date separately.
    def process(date: datetime.date):
        raster = bm_download(gdf, date)
        return raster

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(process, dates)

    # Combine all rasters into a single raster concatenated along time dimension
    combined = xr.concat(results, dim="time", data_vars="minimal", coords="minimal")

    # Store in Zarr format for later
    combined.to_zarr(zarr_path)

    # Loads fresh from disk
    return bm_load_from_zarr(zarr_path)


def bm_load_from_zarr(path: str | Path | None = None) -> xr.Dataset:
    """Load Blackmarble dataset from Zarr store

    :param path: Path to Zarr store, defaults to None
    :raises ValueError: Zarr store does not exist
    :return: Reference to Zarr dataset
    """
    path = Path(path) if path else BM_DATA_DIR / "preprocessed" / f"{BM_PRODUCT}-{BM_VARIABLE}.zarr"

    if not path.exists():
        raise ValueError(f"File does not exist: {path}")

    return xr.open_zarr(path)
