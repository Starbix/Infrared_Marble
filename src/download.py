import sys
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

import geopandas
import requests
from blackmarble.raster import bm_raster
from blackmarble.types import Product
from httpx import HTTPError
from pkg_resources import get_default_cache
from tqdm import tqdm

from utils import BEARER_TOKEN, BLACKMARBLE_DATA_DIR, DATA_DIR

if TYPE_CHECKING:
    from geopandas import GeoDataFrame


def get_gdf(gdf_url: str):
    # We download the file locally to avoid having to download it every time
    gdf_download_path = DATA_DIR / "gdf_files" / gdf_url.split("/")[-1]
    gdf_download_path.parent.mkdir(parents=True, exist_ok=True)

    if not gdf_download_path.exists() or len(gdf_download_path.read_bytes()) < 10:
        print(f"Downloading to {gdf_download_path}")
        response = requests.get(gdf_url, timeout=30.0)
        if response.status_code >= 400:
            raise HTTPError("Failed to download GDF. Please double-check the URL and try again.")
        gdf_download_path.write_bytes(response.content)
        print("GDF successfully downloaded")
    else:
        print("GDF already downloaded, skipping...")
        print("Please delete the file and re-run this cell if the remote data is newer.")

    gdf = geopandas.read_file(gdf_download_path)
    return gdf


def bm_download(gdf: "GeoDataFrame", iso_date: str):
    raster = bm_raster(
        gdf,
        product_id=Product.VNP46A2,
        date_range=date.fromisoformat(iso_date),
        bearer=BEARER_TOKEN,
        output_directory=BLACKMARBLE_DATA_DIR,
        output_skip_if_exists=True,
    )
    return raster


def bm_download_all(gdf_url: str, dates: list[str]):
    date_to_raster = {}

    gdf = get_gdf(gdf_url)

    for date_string in tqdm(dates, desc="PROCESSING DATES"):
        print(f"Downloading raster for {date_string}")
        if not date_string in date_to_raster:
            date_to_raster[date_string] = bm_download(gdf, date_string)

    return date_to_raster
