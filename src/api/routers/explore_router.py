from fastapi import APIRouter
from fastapi.params import Path
from fastapi.responses import FileResponse
from typing_extensions import Annotated

from api.helpers import Resolution, get_admin_area_by_id
from lib.loading import avail_dates
from lib.utils import ADMIN_AREA_FILE_MAPPING

router = APIRouter(prefix="/explore", tags=["Explore"])


@router.get("/dates/{admin_id}")
async def get_dates(admin_id: str):
    # Frontend needs dates sorted in ascending order
    dates = sorted(avail_dates(admin_id))
    return dates


@router.get("/admin-areas")
async def get_admin_areas(resolution: Resolution = "50m"):
    # Validation performed by pydantic thanks to type annotation
    file_path = ADMIN_AREA_FILE_MAPPING[resolution]
    return FileResponse(
        file_path,
        media_type="application/geo+json",
        headers={"Content-Encoding": "gzip"},
    )


@router.get("/admin-areas/{id}")
async def get_admin_area(
    id: Annotated[str, Path()], resolution: Resolution = "50m"
):
    admin_area = get_admin_area_by_id(id, resolution=resolution)
    return admin_area
