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


def bm_dataset_preprocess(
    gdf: "GeoDataFrame",
    dates: list[datetime.date],
    dest: str | Path | None = None,
    force: bool = False,
) -> xr.Dataset:
    # Check if already preprocessed
    zarr_path = Path(dest) if dest else (BM_DATA_DIR / "preprocessed" / f"{BM_PRODUCT}-{BM_VARIABLE}.zarr")
    zarr_path.parent.mkdir(parents=True, exist_ok=True)
    if not force and zarr_path.exists():
        print("Dataset already preprocessed, skipping...")
        return get_bm(zarr_path)

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
    return get_bm(zarr_path)


def get_bm(path: str | Path | None = None):
    path = Path(path) if path else BM_DATA_DIR / "preprocessed" / f"{BM_PRODUCT}-{BM_VARIABLE}.zarr"

    if not path.exists():
        raise ValueError(f"File does not exist: {path}")

    return xr.open_zarr(path)
