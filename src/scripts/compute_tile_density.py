#!/usr/bin/env python3
"""
compute_tile_density_offline.py

Reads image_counts.csv, computes each country's area from Natural Earth
GeoJSON (fetched from GitHub), and calculates:

    CoverageFraction = (Count × 2048×2048 × (129 m)²) / (Country_area_m²)

Outputs: data/luojia/image_counts_with_density.csv

Usage:
    python3 compute_tile_density_offline.py

Dependencies:
    pip install pandas geopandas pyproj shapely
"""

import os
import sys

import geopandas as gpd
import pandas as pd

from lib.config import STATIC_DIR

# ──────────────────────────────────────────────────────────────────────────────
# Adjust these paths to match your setup
CSV_IN = STATIC_DIR / "image_counts.csv"
CSV_OUT = STATIC_DIR / "image_counts_with_density.csv"


# Imaging constants
PIXELS_PER_IMAGE = 2048 * 2048
PIXEL_SIZE_M = 129  # meters per pixel
PIXEL_AREA_M2 = PIXEL_SIZE_M**2  # m² per pixel

# … earlier imports …

# A small name-override map so our CSV’s “Country” matches the GeoJSON’s “ADMIN”
NAME_OVERRIDES = {
    "United States": "United States of America",
    "Korea, Republic of": "South Korea",
    "Taiwan, Province of China": "Taiwan",
    "Korea, Democratic People's Republic of": "North Korea",
    "Russian Federation": "Russia",
    "Serbia": "Republic of Serbia",
    "Türkiye": "Turkey",
    "Montenegro, Republic of": "Montenegro",
    "North Macedonia, Republic of": "North Macedonia",
    "Viet Nam": "Vietnam",
    "Macao": "China",
    "Syrian Arab Republic": "Syria",
    "Czech Republic": "Czechia",
    "Iran, Islamic Republic of": "Iran",
    "Hong Kong": "China",
    "Aland Islands": "Aland Islands",
    "Lao People's Democratic Republic": "Laos",
    "Brunei Darussalam": "Brunei",
    # keep any existing overrides below…
}


def load_country_areas() -> pd.DataFrame:
    """
    Fetch Natural Earth–derived GeoJSON from GitHub, detect the country-name
    and ISO-A2 columns dynamically, reproject to equal-area CRS,
    compute area_km2, and return a DataFrame with columns:
       lookup_name, iso_a2, area_km2
    """
    GEOJSON_URL = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
    world = gpd.read_file(GEOJSON_URL)

    # reproject so .area is in meters², then convert to km²
    world_eq = world.to_crs("EPSG:6933")
    world_eq["area_km2"] = world_eq.geometry.area / 1e6

    cols = list(world_eq.columns)
    # pick the first column whose name contains "admin" or "name" as the country name
    name_cols = [c for c in cols if "admin" in c.lower() or "name" == c.lower()]
    # pick the first column containing "iso" and length ≤ 5 as the iso code
    iso_cols = [c for c in cols if "iso" in c.lower()]

    if not name_cols or not iso_cols:
        raise RuntimeError(f"Could not detect country-name or iso columns in {cols}")

    name_col = name_cols[0]
    iso_a2 = [c for c in iso_cols if c.endswith("2")][0]
    iso_a3 = [c for c in iso_cols if c.endswith("3")][0]

    # slice down to just those three
    df = world_eq[[name_col, iso_a2, iso_a3, "area_km2"]].copy()
    df.columns = ["lookup_name", "iso_a2", "iso_a3", "area_km2"]
    return df


def main():
    # 1) load your image-counts CSV
    if not os.path.isfile(CSV_IN):
        print(f"Error: cannot find {CSV_IN}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(CSV_IN, dtype={"Country": str})
    if not {"Date", "Country", "Count"}.issubset(df.columns):
        print("Error: CSV must have Date, Country, Count", file=sys.stderr)
        sys.exit(1)

    # 2) load country areas from GeoJSON
    areas_gdf = load_country_areas()

    # 3) map your CSV’s Country → GeoJSON lookup_name
    df["lookup_name"] = df["Country"].map(lambda c: NAME_OVERRIDES.get(c, c))

    # 4) merge on lookup_name
    merged = pd.merge(df, areas_gdf, on="lookup_name", how="left", validate="m:1")

    # 5) warn if any didn’t match
    missing = merged[merged["area_km2"].isna()]["Country"].unique()
    if len(missing):
        print("Warning: no area found for:", ", ".join(missing), file=sys.stderr)

    # 6) compute coverage fraction
    merged["Tiles"] = merged["Count"] * PIXELS_PER_IMAGE
    merged["Covered_m2"] = merged["Tiles"] * PIXEL_AREA_M2
    merged["Country_m2"] = merged["area_km2"] * 1e6
    merged["CoverageFraction"] = merged["Covered_m2"] / merged["Country_m2"]

    # 7) write out
    out = merged.rename(columns={"area_km2": "Area_km2", "iso_a3": "ISO_A3"})
    out[["Date", "ISO_A3", "Country", "Count", "Area_km2", "CoverageFraction"]].to_csv(
        CSV_OUT, index=False, float_format="%.8f"
    )

    print(f"✔ Wrote {len(out)} rows to {CSV_OUT}")
    print("Preview:")
    print(out[["Date", "ISO_A3", "Country", "Count", "Area_km2", "CoverageFraction"]].head().to_string(index=False))


if __name__ == "__main__":
    main()
