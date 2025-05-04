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


def bm_geotiff_task(gdf: geopandas.GeoDataFrame, date: date):
    bm_data = bm_download(gdf, date)
    return bm_data


@router.get("/bm")
async def get_bm_geotiff(
    date: date,
    admin_id: str,
    executor: Annotated[ProcessPoolExecutor, Depends(get_executor)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    nocache: bool = False,
):
    with gzip.open(ADMIN_AREA_FILE_MAPPING["50m"]) as f:
        gdf = geopandas.read_file(f)
    gdf = gdf[gdf[GEOJSON_ADMIN_KEY] == admin_id]
    assert isinstance(gdf, geopandas.GeoDataFrame)

    # Generate xarray
    cache_key = f"bm:{date}:{admin_id}"
    cached_data = redis_client.get(cache_key)
    if nocache:
        redis_client.delete(cache_key)
    if not nocache and cached_data:
        raster = pickle.loads(cached_data)
    else:
        future = executor.submit(bm_geotiff_task, gdf, date)
        raster = future.result()
        raster_serialized = pickle.dumps(raster)
        redis_client.set(cache_key, raster_serialized)

    # Convert xarray to GeoTIFF and return
    with io.BytesIO() as buf:
        data_array = raster["Gap_Filled_DNB_BRDF-Corrected_NTL"].rio.write_crs("EPSG:4326")
        data_array = data_array.rio.clip(gdf.geometry.values, gdf.crs, drop=True)
        pc02 = float(data_array.quantile(0.02).values)
        pc98 = float(data_array.quantile(0.98).values)
        data_array.rio.to_raster(buf, driver="GTiff", compress="LZW")
        buf.seek(0)
        content = buf.getvalue()
    # We return some metadata in the headers as we can't use GDAL metadata on client
    headers = {
        "Access-Control-Expose-Headers": "*",  # Required for CORS
        "X-Raster-P02": str(pc02),
        "X-Raster-P98": str(pc98),
    }
    return Response(content=content, media_type="image/tiff", headers=headers)
