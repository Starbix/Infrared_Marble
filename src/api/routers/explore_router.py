from typing import Literal

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from lib.misc import list_dates
from lib.utils import ADMIN_AREA_FILE_MAPPING

router = APIRouter(prefix="/explore", tags=["Explore"])


@router.get("/dates")
async def get_dates():
    # Frontend needs dates sorted in ascending order
    dates = sorted(list_dates())
    return dates


@router.get("/admin-areas")
async def get_admin_areas(resolution: Literal["110m", "50m", "10m"] = "50m"):
    # Validation performed by pydantic thanks to type annotation
    file_path = ADMIN_AREA_FILE_MAPPING[resolution]
    return FileResponse(
        file_path,
        media_type="application/geo+json",
        headers={"Content-Encoding": "gzip"},
    )
