from pathlib import Path

import numpy as np
import pandas as pd
import xarray

from lib.utils import BM_DATA_DIR, BM_PRODUCT, BM_VARIABLE, STATIC_DIR


def get_bm(path: str | Path | None = None):
    path = (
        Path(path)
        if path
        else BM_DATA_DIR / "preprocessed" / f"{BM_PRODUCT}-{BM_VARIABLE}.zarr"
    )

    if not path.exists():
        raise ValueError(f"File does not exist: {path}")

    return xarray.open_zarr(path)


def avail_dates(admin_id: str):
    country_meta = pd.read_csv(STATIC_DIR / "country_meta.csv.gz")
    dates = country_meta[country_meta["country"] == admin_id]["date"]
    return np.unique(dates)
