import gzip
from pathlib import Path

import geopandas
import numpy as np
import pandas as pd
import xarray

from lib.constants import (
    ADMIN_AREA_FILE_MAPPING,
    BM_DATA_DIR,
    BM_PRODUCT,
    BM_VARIABLE,
    GEOJSON_ADMIN_KEY,
    STATIC_DIR,
)


def get_bm(path: str | Path | None = None):
    path = Path(path) if path else BM_DATA_DIR / "preprocessed" / f"{BM_PRODUCT}-{BM_VARIABLE}.zarr"

    if not path.exists():
        raise ValueError(f"File does not exist: {path}")

    return xarray.open_zarr(path)


def avail_dates(admin_id: str):
    country_meta = pd.read_csv(STATIC_DIR / "country_meta.csv.gz")
    dates = country_meta[country_meta["country"] == admin_id]["date"]
    return np.unique(dates)


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


def load_all_dates(path: str | Path | None = None):
    path = Path(path) if path else STATIC_DIR / "all_dates.csv"
    return pd.read_csv(path, compression="infer")
