from fastapi import APIRouter, HTTPException

from lib.loading import load_all_dates, load_country_meta
from lib.utils import ADMIN_AREA_FILE_MAPPING

router = APIRouter(prefix="/statistics", tags=["Explore"])


@router.get("/summary")
async def get_statistics():
    """
    Get statistics for the dataset.
    """
    country_meta = load_country_meta()
    dates = load_all_dates()

    return {
        "general": {"geojson_resolutions": len(ADMIN_AREA_FILE_MAPPING)},
        "luojia": {
            "total_images": len(country_meta),
            "total_admin_areas": len(country_meta["country"].unique()),
            "total_dates": len(dates),
        },
    }


@router.get("/dates/{admin_id}")
async def get_region_dates(admin_id: str):
    """
    Get a list of dates where the region has data.
    """
    admin_meta = load_country_meta()

    admin_data = admin_meta[admin_meta["country"] == admin_id]
    if admin_data.empty:
        raise HTTPException(status_code=404, detail="Admin area not found")

    return {"admin_id": admin_id, "dates": sorted(admin_data["date"].unique())}
