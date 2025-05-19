import datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal, overload

import geopandas
import xarray as xr
from blackmarble.raster import bm_raster
from blackmarble.types import Product
from geopandas import GeoDataFrame

from lib.admin_areas import get_region_gdf
from lib.config import (
    BM_DATA_DIR,
    BM_DEFAULT_PRODUCT,
    BM_DEFAULT_QUALITY_FLAG,
    BM_DEFAULT_VARIABLE,
    BM_TOKEN,
)
from lib.types import Resolution, VNP46A1_Variable, VNP46A2_Variable


def bm_get_unified_gdf(
    admin_id: str, date: str | datetime.date, resolution: Resolution = "50m", merge_luojia_geometry: bool = True
):
    if isinstance(date, datetime.date):
        date = date.isoformat()

    gdf = get_region_gdf(admin_id, resolution=resolution)

    if merge_luojia_geometry:
        print(f"Merging LuoJia geometry for {admin_id} on {date}")
        # Get and merge LuoJia geometry
        import pandas as pd

        from .lj import lj_get_region_geometry

        geometry = lj_get_region_geometry(admin_id, date)
        gdf_lj = geopandas.GeoDataFrame(geometry=[geometry], crs=gdf.crs)
        all_geoms = pd.concat([gdf.geometry, gdf_lj.geometry])
        geom_merged = all_geoms.union_all(method="unary")
        gdf = geopandas.GeoDataFrame(geometry=[geom_merged], crs=gdf.crs)

    return gdf


# Provide overloads for "variable" type hints
@overload
def bm_download(
    gdf: GeoDataFrame,
    date_range: datetime.date | list[datetime.date],
    product: Literal[Product.VNP46A1],
    variable: VNP46A1_Variable,
    drop_values_by_quality_flag: list[int] | None = None,
    use_cache: bool = True,
) -> xr.Dataset: ...


@overload
def bm_download(
    gdf: GeoDataFrame,
    date_range: datetime.date | list[datetime.date],
    product: Literal[Product.VNP46A2],
    variable: VNP46A2_Variable,
    drop_values_by_quality_flag: list[int] | None = None,
    use_cache: bool = True,
) -> xr.Dataset: ...


def bm_download(
    gdf: "GeoDataFrame",
    date_range: datetime.date | list[datetime.date],
    product: Product,
    variable: VNP46A1_Variable | VNP46A2_Variable,
    drop_values_by_quality_flag: list[int] | None = None,
    use_cache: bool = True,
) -> xr.Dataset:
    """Downloads data from Blackmarble dataset for a given region and date range.

    :param gdf: GeoDataFrame of region of interest
    :param date_range: Single date or list of dates to download data for
    :return: xarray.Dataset containing raster data
    """
    out_dir = BM_DATA_DIR / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    raster = bm_raster(
        gdf,
        product_id=product,
        date_range=date_range,
        bearer=BM_TOKEN,
        output_directory=out_dir,
        drop_values_by_quality_flag=drop_values_by_quality_flag or BM_DEFAULT_QUALITY_FLAG,
        variable=variable,
        output_skip_if_exists=use_cache,
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
    zarr_path = (
        Path(dest) if dest else (BM_DATA_DIR / "preprocessed" / f"{BM_DEFAULT_PRODUCT}-{BM_DEFAULT_VARIABLE}.zarr")
    )
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
    path = Path(path) if path else BM_DATA_DIR / "preprocessed" / f"{BM_DEFAULT_PRODUCT}-{BM_DEFAULT_VARIABLE}.zarr"

    if not path.exists():
        raise ValueError(f"File does not exist: {path}")

    return xr.open_zarr(path)
