from fastapi import APIRouter

from lib.misc import list_dates
from lib.utils import PROJECT_ROOT

router = APIRouter(prefix="/explore", tags=["Explore"])


@router.get("/dates")
async def get_dates():
    print("PROJECT_ROOT:", PROJECT_ROOT)
    dates = list_dates()
    return dates
