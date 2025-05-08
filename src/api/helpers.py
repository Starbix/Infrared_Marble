import gzip
import json
from typing import Any

from fastapi.exceptions import HTTPException

from lib.constants import ADMIN_AREA_FILE_MAPPING, GEOJSON_ADMIN_KEY
from lib.types import Resolution


def get_admin_area_by_id(id: str, resolution: Resolution = "50m") -> dict[str, Any]:
    file_path = ADMIN_AREA_FILE_MAPPING[resolution]
    # Need to filter admin areas and get correct feature out

    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        geojson_data = json.load(f)

    filtered_features = [
        feature for feature in geojson_data["features"] if feature["properties"].get(GEOJSON_ADMIN_KEY) == id
    ]

    if len(filtered_features) == 0:
        raise HTTPException(status_code=404, detail=f"Admin area with ID `{id}` not found.")
    if len(filtered_features) > 1:
        raise HTTPException(status_code=400, detail="More than one admin areas match given ID")

    return filtered_features[0]
