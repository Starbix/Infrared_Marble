import numpy as np
import pandas as pd
import pycountry
from fastapi import APIRouter, HTTPException

from lib.admin_areas import (
    dates_from_csv,
    get_all_regions_gdf,
    get_region_avail_dates,
    get_region_meta,
    get_tile_densities,
)
from lib.cloud_coverage import get_day_cloud_coverage
from lib.config import ADMIN_AREA_FILE_MAPPING, GEOJSON_ADMIN_KEY, STATIC_DIR

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("/summary")
async def get_statistics():
    """
    Get statistics for the dataset.
    """
    country_meta = get_region_meta()
    dates = dates_from_csv(filename=STATIC_DIR / "all_dates.csv")

    return {
        "general": {"geojson_resolutions": len(ADMIN_AREA_FILE_MAPPING)},
        "luojia": {
            "total_images": len(country_meta),
            "total_admin_areas": len(country_meta["country"].unique()),
            "total_dates": len(dates),
        },
    }


@router.get("/regions")
async def get_regions():
    gdf = get_all_regions_gdf()
    region_meta = get_region_meta()
    avail_regions = region_meta["country"].unique()
    regions = gdf[[GEOJSON_ADMIN_KEY, "name"]].drop_duplicates()
    regions = regions[regions[GEOJSON_ADMIN_KEY].isin(avail_regions)]
    regions = regions.rename(columns={GEOJSON_ADMIN_KEY: "admin_id"})
    regions = regions.sort_values(by="admin_id")
    return regions.to_dict(orient="records")


@router.get("/heatmap/{admin_id}")
async def get_region_dates(admin_id: str):
    """
    Gets a heatmap of the region, where the available dates are binned into monthly intervals. Each row is a year of
    data, and each column is a month of the year. The data ranges over all contained years in the available dates.
    """
    admin_meta = get_region_meta()

    admin_data = admin_meta[admin_meta["country"] == admin_id]
    if admin_data.empty:
        raise HTTPException(status_code=404, detail="Admin area not found")

    # Convert dates to datetime objects
    admin_data["date"] = pd.to_datetime(admin_data["date"])
    admin_data["year"] = admin_data["date"].dt.year
    admin_data["month"] = admin_data["date"].dt.month

    # Compute monthly counts
    monthly_count = admin_data.groupby(["year", "month"]).size().reset_index(name="count")

    # Create heatmap grid
    years = list(range(admin_data["year"].min(), admin_data["year"].max() + 1))
    months = list(range(1, 13))
    index = pd.MultiIndex.from_product([years, months], names=["year", "month"])
    heatmap = pd.DataFrame(index=index, columns=["count"]).fillna(0)
    heatmap.update(monthly_count.set_index(["year", "month"]))

    # Get heatmap as 2D array where first dimension is years and second dimension is months
    heatmap = heatmap["count"].unstack().values.tolist()

    return {
        "stats": {
            "min_year": years[0],
            "max_year": years[-1],
            "unique_dates": admin_data["date"].nunique(),
            "total_tiles": len(admin_data),
        },
        "years": years,
        "months": months,
        "heatmap": heatmap,
    }


@router.get("/clouds/{admin_id}")
async def get_stats_admin_area(admin_id: str):
    """
    Get cloud coverage for an admin area.
    """
    country_name = pycountry.countries.get(alpha_3=admin_id.upper()).name  # type: ignore
    dates = get_region_avail_dates(admin_id)
    dates_clouds = {}
    for date in dates:
        lj, bm = get_day_cloud_coverage(date, country_name)
        dates_clouds[date] = {"lj_cloud_coverage": lj, "bm_cloud_coverage": bm}

    return dates_clouds


@router.get("/coverage-fraction")
async def get_coverage_fraction():
    df = get_tile_densities()

    # Return average country coverage over all dates where data is available
    coverage = df.groupby("ISO_A3")["CoverageFraction"].mean().sort_values(ascending=False)
    log_coverage = pd.Series(np.log10(coverage))

    # Compute percentiles
    pc02, pc98 = log_coverage.quantile(q=[0.02, 0.98])

    # Compute ticks
    tickvals = np.linspace(pc02, pc98, num=5)
    ticklabels = 10**tickvals

    return {
        "index": coverage.index.tolist(),
        "coverage": coverage.tolist(),
        "log_coverage": np.log10(coverage).tolist(),
        "scale": {
            "tickvals": tickvals.tolist(),
            "ticklabels": ticklabels.tolist(),
        },
        "stats": {
            "zmin": pc02,
            "zmax": pc98,
        },
    }
