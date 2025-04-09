from pathlib import Path

import xarray

from utils import BM_DATA_DIR


def get_bm(path: str | Path | None = None):
    path = Path(path) if path else BM_DATA_DIR / "preprocessed" / "dataset.zarr"

    if not path.exists():
        raise ValueError("File does not exist:", path)

    return xarray.open_zarr(path)
