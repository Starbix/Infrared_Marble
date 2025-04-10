import datetime
import tarfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TYPE_CHECKING

import geopandas
import httpx
import requests
import xarray as xr
from blackmarble.raster import bm_raster
from httpx import HTTPError
from tqdm import tqdm

from lib.loading import get_bm
from lib.utils import (
    BEARER_TOKEN,
    BM_DATA_DIR,
    BM_PRODUCT,
    BM_QUALITY_FLAG,
    BM_VARIABLE,
    DATA_DIR,
    LJ_DATA_DIR,
)

if TYPE_CHECKING:
    from geopandas import GeoDataFrame


def fetch_gdf(gdf_url: str, force: bool = False):
    # We download the file locally to avoid having to download it every time
    gdf_download_path = DATA_DIR / "gdf_files" / gdf_url.split("/")[-1]
    gdf_download_path.parent.mkdir(parents=True, exist_ok=True)

    if force or not gdf_download_path.exists() or len(gdf_download_path.read_bytes()) < 10:
        print(f"Downloading to {gdf_download_path}")
        response = requests.get(gdf_url, timeout=30.0)
        if response.status_code >= 400:
            raise HTTPError("Failed to download GDF. Please double-check the URL and try again.")
        gdf_download_path.write_bytes(response.content)
        print("GDF successfully downloaded")
    else:
        print("GDF already downloaded, skipping... (use --force to re-download)")

    gdf = geopandas.read_file(gdf_download_path)
    return gdf


def get_dates(file: str | Path) -> list[datetime.date]:
    file = Path(file)

    if not file.exists():
        raise ValueError(f"File does not exist: {file}")

    return sorted([datetime.date.fromisoformat(l.strip()) for l in file.read_text().splitlines()])


def bm_download(gdf: "GeoDataFrame", date_range: datetime.date | list[datetime.date]) -> xr.Dataset:
    out_dir = BM_DATA_DIR / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    raster = bm_raster(
        gdf,
        product_id=BM_PRODUCT,
        date_range=date_range,
        bearer=BEARER_TOKEN,
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
    zarr_path = (
        Path(dest) if dest else (BM_DATA_DIR / "preprocessed" / f"dataset-{BM_PRODUCT}.zarr")
    )
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
