from fastapi import APIRouter

from lib.misc import list_dates

router = APIRouter(prefix="/explore", tags=["Explore"])


@router.get("/dates")
async def get_dates():
    # Frontend needs dates sorted in ascending order
    dates = sorted(list_dates())
    return dates
