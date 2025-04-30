from fastapi import APIRouter

from api.types import DatasetName

router = APIRouter(prefix="/explore", tags=["Explore"])


@router.get("/explore/dates/{dataset}")
async def get_dates(dataset: DatasetName):
    if dataset == DatasetName.blackmarble:
        return "all dates"
    if dataset == DatasetName.luojia:
        return ["2020-01-01", "2021-03-27"]
