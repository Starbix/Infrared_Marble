import datetime
import gzip
from pathlib import Path

import geopandas
import numpy as np
import pandas as pd
import requests

from lib.config import ADMIN_AREA_FILE_MAPPING, DATA_DIR, DEFAULT_DATES_FILE, GEOJSON_ADMIN_KEY, STATIC_DIR


def get_dates(file: str | Path) -> list[datetime.date]:
    file = Path(file)

    if not file.exists():
        raise ValueError(f"File does not exist: {file}")

    df = pd.read_csv(file)
    date_list = [datetime.date.fromisoformat(d) for d in df["date"].dropna()]

    return sorted(date_list)


def list_dates(file: str | Path | None = None):
    file = Path(file) if file else DEFAULT_DATES_FILE

    if not file.exists():
        raise ValueError(f"File does not exist: {file}")

    dates = get_dates(file)

    return dates


def avail_dates(admin_id: str):
    country_meta = pd.read_csv(STATIC_DIR / "country_meta.csv.gz")
    dates = country_meta[country_meta["country"] == admin_id]["date"]
    return np.unique(dates)


def load_all_dates(path: str | Path | None = None):
    path = Path(path) if path else STATIC_DIR / "all_dates.csv"
    return pd.read_csv(path, compression="infer")


def fetch_gdf(gdf_url: str, force: bool = False):
    # We download the file locally to avoid having to download it every time
    gdf_download_path = DATA_DIR / "gdf_files" / gdf_url.split("/")[-1]
    gdf_download_path.parent.mkdir(parents=True, exist_ok=True)

    if force or not gdf_download_path.exists() or len(gdf_download_path.read_bytes()) < 10:
        print(f"Downloading to {gdf_download_path}")
        response = requests.get(gdf_url, timeout=30.0)
        if response.status_code >= 400:
            raise requests.HTTPError("Failed to download GDF. Please double-check the URL and try again.")
        gdf_download_path.write_bytes(response.content)
        print("GDF successfully downloaded")
    else:
        print("GDF already downloaded, skipping... (use --force to re-download)")

    gdf = geopandas.read_file(gdf_download_path)
    return gdf


def get_all_regions_gdf():
    with gzip.open(ADMIN_AREA_FILE_MAPPING["50m"]) as f:
        return geopandas.read_file(f)


def get_region_gdf(admin_id: str):
    with gzip.open(ADMIN_AREA_FILE_MAPPING["50m"]) as f:
        gdf = geopandas.read_file(f)
    gdf = gdf[gdf[GEOJSON_ADMIN_KEY] == admin_id]
    assert isinstance(gdf, geopandas.GeoDataFrame)
    return gdf


def load_country_meta(path: str | Path | None = None):
    path = Path(path) if path else STATIC_DIR / "country_meta.csv.gz"
    return pd.read_csv(path, compression="infer")
