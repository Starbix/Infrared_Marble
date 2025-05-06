from fastapi import APIRouter
from fastapi.params import Path
from fastapi.responses import FileResponse
from typing_extensions import Annotated

from api.helpers import Resolution, get_admin_area_by_id
from lib.misc import list_dates
from lib.utils import ADMIN_AREA_FILE_MAPPING

router = APIRouter(prefix="/explore", tags=["Explore"])


@router.get("/statistics/")
async def get_statistics():
    """
    Get statistics for the dataset.
    """
    return {
        "total_images": 1000,
        "total_admin_areas": 100,
        "total_dates": len(list_dates()),
        "total_resolutions": len(ADMIN_AREA_FILE_MAPPING),
    }
