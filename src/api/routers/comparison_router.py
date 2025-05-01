from datetime import datetime
from typing import Annotated
from fastapi.params import Path
from fastapi.routing import APIRouter
import geopandas
import gzip

from lib.download import bm_download
from lib.utils import ADMIN_AREA_FILE_MAPPING


router = APIRouter(prefix="/compare/{date}/{adminId}", tags=["Compare"])


@router.get("/bm")
async def get_bm_geotiff(date: Annotated[datetime, Path()], adminId: str):
    with gzip.open(ADMIN_AREA_FILE_MAPPING["50m"]) as f:
        gdf = geopandas.read_file(f)
    gdf_admin = gdf[gdf["adm0_a3"] == adminId]
    bm_data = bm_download(gdf_admin, date.date())
    print("Got BM data:", bm_data)
    return bm_data
