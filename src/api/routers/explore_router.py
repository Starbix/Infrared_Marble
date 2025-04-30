from fastapi import APIRouter
from fastapi.responses import FileResponse

from lib.misc import list_dates
from lib.utils import ALL_ADMIN_AREAS_GEOJSON_FILE

router = APIRouter(prefix="/explore", tags=["Explore"])


@router.get("/dates")
async def get_dates():
    # Frontend needs dates sorted in ascending order
    dates = sorted(list_dates())
    return dates


@router.get('/admin-areas')
async def get_admin_areas():
    return FileResponse(
        ALL_ADMIN_AREAS_GEOJSON_FILE,
        media_type='application/geo+json',
        headers={
            'Content-Encoding': 'gzip'
        }
    )
