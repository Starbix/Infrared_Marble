from concurrent.futures import ProcessPoolExecutor
from datetime import date
import io
from typing import Annotated
from fastapi import Depends, Response
from fastapi.routing import APIRouter
import geopandas
import gzip
import pickle

from redis import Redis

from api.dependencies import get_executor, get_redis_client
from lib.download import bm_download
from lib.utils import ADMIN_AREA_FILE_MAPPING, GEOJSON_ADMIN_KEY


router = APIRouter(prefix="/compare/{date}/{admin_id}", tags=["Compare"])


def bm_geotiff_task(date: date, admin_id: str):
    with gzip.open(ADMIN_AREA_FILE_MAPPING["50m"]) as f:
        gdf = geopandas.read_file(f)
    gdf_admin = gdf[gdf[GEOJSON_ADMIN_KEY] == admin_id]
    bm_data = bm_download(gdf_admin, date)
    return bm_data


@router.get("/bm")
async def get_bm_geotiff(
    date: date,
    admin_id: str,
    executor: Annotated[ProcessPoolExecutor, Depends(get_executor)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
):
    # Generate xarray
    cache_key = f"bm:{date}:{admin_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        raster = pickle.loads(cached_data)
    else:
        future = executor.submit(bm_geotiff_task, date, admin_id)
        raster = future.result()
        raster_serialized = pickle.dumps(raster)
        redis_client.set(cache_key, raster_serialized)

    # Convert xarray to GeoTIFF and return
    with io.BytesIO() as buf:
        raster["Gap_Filled_DNB_BRDF-Corrected_NTL"].rio.to_raster(buf, driver="GTiff", compress="LZW")
        buf.seek(0)
        content = buf.getvalue()
    return Response(content=content, media_type="image/tiff")
