import io
import logging
import pickle
from concurrent.futures import ThreadPoolExecutor
from datetime import date

import geopandas
import xarray as xr
from fastapi import Response
from fastapi.concurrency import run_in_threadpool
from fastapi.routing import APIRouter

from lib.constants import BM_DATA_DIR, LJ_DATA_DIR
from lib.download import bm_download, luojia_tile_download
from lib.geotiff import get_geotiffs, merge_geotiffs, resample_geotiff
from lib.loading import get_region_gdf, load_country_meta

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/compare/{date}/{admin_id}", tags=["Compare"])


def bm_geotiff_task(gdf: geopandas.GeoDataFrame, date: date):
    bm_data = bm_download(gdf, date)
    return bm_data


# directly returns GeoTIFF
def lj_geotiff_task(gdf: geopandas.GeoDataFrame, date: date):
    geotiff_list = get_geotiffs(gdf, date)
    for geotiff in geotiff_list:
        luojia_tile_download(geotiff)

    geotiff_buf, pc02, pc98 = merge_geotiffs(geotiff_list)

    return geotiff_buf, pc02, pc98


@router.get("/bm")
async def get_bm_geotiff_new(
    date: date,
    admin_id: str,
    variable: str = "Gap_Filled_DNB_BRDF-Corrected_NTL",
    crs: str = "EPSG:4326",
    nocache: bool = False,
):
    cache_dir = BM_DATA_DIR / "cache" / admin_id / date.isoformat() / variable
    raster_path = cache_dir / "raster.tif"
    meta_path = cache_dir / "meta.pkl"

    # Try to load from cache first
    geotiff_buf, pc02, pc98 = None, None, None
    if not nocache and cache_dir.exists():
        logger.info("BM: Loading (%s, %s) from cache", admin_id, date.isoformat())
        geotiff_buf = raster_path.read_bytes()
        meta = pickle.loads(meta_path.read_bytes())
        pc02, pc98 = meta["pc02"], meta["pc98"]

    if not nocache and cache_dir.exists() and cache_dir.is_dir():
        try:
            logger.info("Loading BM raster (%s, %s) from cache", admin_id, date.isoformat())
            dataset = xr.load_dataset(cache_dir, engine="zarr", mode="r")
        except Exception as e:
            logger.warning(
                "Zarr file exists but failed to open. The file is possibly corrupted. (Looking up %s)", cache_dir
            )
            logger.warning("Error from previous call: %s", str(e))
            dataset = None

    # Download if not available in cache
    if geotiff_buf is None or pc02 is None or pc98 is None:
        logger.info("BM: Downloading (%s, %s)", admin_id, date.isoformat())
        gdf = get_region_gdf(admin_id)
        dataset = await run_in_threadpool(bm_download, gdf=gdf, date_range=date)
        dataset.to_zarr(cache_dir, mode="w")
        logger.info("Download complete.")

        # Convert dataset to GeoTIFF response
        logger.info("Writing CRS...")
        data_array = dataset[variable].rio.write_crs(crs)

        # Create GeoTIFF in memory
        logger.info("Converting to raster...")
        with io.BytesIO() as buf:
            data_array.rio.to_raster(
                buf,
                driver="GTiff",
                compress="LZW",
                tiled=True,
                blockxsize=256,
                blockysize=256,
                windowed=True,
            )
            buf.seek(0)
            geotiff_buf = buf.getvalue()

        # Calculate stats for headers
        logger.info("Computing quantiles...")
        pc02 = float(data_array.quantile(0.02).values)
        pc98 = float(data_array.quantile(0.98).values)

        # Store in cache
        cache_dir.mkdir(parents=True, exist_ok=True)
        raster_path.write_bytes(geotiff_buf)
        meta_path.write_bytes(pickle.dumps({"pc02": pc02, "pc98": pc98}))

    # Create response with headers
    headers = {
        "Access-Control-Expose-Headers": "*",  # Required for CORS
        "X-Raster-P02": str(pc02),
        "X-Raster-P98": str(pc98),
    }

    return Response(geotiff_buf, media_type="image/tiff", headers=headers)


def lj_download(
    relevant_tiles: list[str], resample: tuple[float, float] | None = None, parallel_downloads: int | None = None
):
    # Download all GeoTIFFs
    logger.info("Downloading %d tiles", len(relevant_tiles))

    if parallel_downloads:
        with ThreadPoolExecutor(max_workers=parallel_downloads) as executor:
            # Submit all download jobs to the executor
            list(executor.map(luojia_tile_download, relevant_tiles))
    else:
        for tile_name in relevant_tiles:
            luojia_tile_download(tile_name)

    # Merge
    logger.info("Merging tiles...")
    geotiff_buf, pc02, pc98 = merge_geotiffs(relevant_tiles)

    # Resample
    if resample:
        geotiff_buf = resample_geotiff(geotiff_buf, resolution=resample)

    return geotiff_buf, pc02, pc98


@router.get("/lj")
async def get_lj_geotiff(
    date: date,
    admin_id: str,
    variable: str = "default",
    crs: str = "EPSG:4326",
    nocache: bool = False,
):
    resample = None  # No resampling
    cache_dir = LJ_DATA_DIR / "cache" / admin_id / date.isoformat() / variable
    raster_path = cache_dir / f"raster_{'x'.join(resample) if resample else 'default'}.tif"
    meta_path = cache_dir / "meta.pkl"

    # Check if cache exists
    geotiff_buf, pc02, pc98 = None, None, None
    if not nocache and cache_dir.exists():
        logger.info("LJ: Reading (%s, %s) from cache", admin_id, date.isoformat())
        geotiff_buf = raster_path.read_bytes()
        meta = pickle.loads(meta_path.read_bytes())
        pc02, pc98 = meta["pc02"], meta["pc98"]

    # If not cached, download
    if geotiff_buf is None or pc02 is None or pc98 is None:
        logger.info("LJ: Downloading (%s, %s)", admin_id, date.isoformat())
        # Get region meta dataframe
        region_meta = load_country_meta()
        # Select only rows where region and date match
        relevant_tiles = region_meta[(region_meta["country"] == admin_id) & (region_meta["date"] == date.isoformat())]
        relevant_tiles = relevant_tiles["tile_name"].values.tolist()
        geotiff_buf, pc02, pc98 = await run_in_threadpool(
            lj_download, relevant_tiles, resample=resample, parallel_downloads=8
        )
        # Store in cache
        cache_dir.mkdir(parents=True, exist_ok=True)
        raster_path.write_bytes(geotiff_buf)
        meta_path.write_bytes(pickle.dumps({"pc02": pc02, "pc98": pc98}))

    # We return some metadata in the headers as we can't use GDAL metadata on client
    headers = {
        "Access-Control-Expose-Headers": "*",  # Required for CORS
        "X-Raster-P02": str(pc02),
        "X-Raster-P98": str(pc98),
    }
    return Response(content=geotiff_buf, media_type="image/tiff", headers=headers)
