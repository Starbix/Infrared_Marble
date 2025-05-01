from typing import Literal
from fastapi.params import Path
from typing_extensions import Annotated
import json
import gzip

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


Resolution = Literal["110m", "50m", "10m"]


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
async def get_admin_area_by_id(
    id: Annotated[str, Path()], resolution: Resolution = "50m"
):
    file_path = ADMIN_AREA_FILE_MAPPING[resolution]
    # Need to filter admin areas and get correct feature out

    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        geojson_data = json.load(f)

    filtered_features = [
        feature
        for feature in geojson_data["features"]
        if feature["properties"].get("adm0_a3") == id
    ]

    if len(filtered_features) == 0:
        raise HTTPException(
            status_code=404, detail=f"Admin area with ID `{id}` not found."
        )
    if len(filtered_features) > 1:
        raise HTTPException(
            status_code=400, detail="More than one admin areas match given ID"
        )
    return filtered_features[0]
