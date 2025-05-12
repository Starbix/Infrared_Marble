import os
import sys
from pathlib import Path

from blackmarble.types import Product

from lib.types import Resolution

# Note: This code runs whenever the module is first imported.
# This is to make sure that the DATA_DIR and BEARER_TOKEN variables are appropriately set.

# Project/general constants
PROJECT_ROOT = Path(__file__).parents[2]
STATIC_DIR = PROJECT_ROOT / "static"
DATA_DIR = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))

# Blackmarble constants
# Get Bearer token from environment
BM_TOKEN = os.getenv("BLACKMARBLE_TOKEN", "")
BM_DATA_DIR = DATA_DIR / "blackmarble"
BM_PRODUCT = Product(os.environ.get("BM_PRODUCT", Product.VNP46A2))
BM_VARIABLE: str | None = os.environ.get("BM_VARIABLE")  # Default varible for product
BM_QUALITY_FLAG = [int(x) for x in os.environ.get("BM_QUALITY_FLAG", "255").split(",")]
BM_DEFAULT_VARIABLE: dict[Product, str] = {
    Product.VNP46A1: "DNB_At_Sensor_Radiance_500m",
    Product.VNP46A2: "Gap_Filled_DNB_BRDF-Corrected_NTL",
    Product.VNP46A3: "NearNadir_Composite_Snow_Free",
    Product.VNP46A4: "NearNadir_Composite_Snow_Free",
}

# LuoJia constants
LJ_DATA_DIR = DATA_DIR / "luojia"
LJ_DEFAULT_IDS_FILE = STATIC_DIR / "luojia_image_ids.csv"
LJ_TILE_URL_PREFIX = "https://polybox.ethz.ch/index.php/s/dnP82nHZkjR4gr7/download/file?path=%2F"
LJ_METADATA_URL = "https://polybox.ethz.ch/index.php/s/dnP82nHZkjR4gr7/download/file?path=%2Fmetadata%2FMETA.tar.gz"

# GeoJSON, dates, etc
DEFAULT_DATES_FILE = STATIC_DIR / "defaults" / "dates_luojia_myanmar.csv"
DEFAULT_GDF_FILE = "gadm41_MMR_1.geojson.gz"
ADMIN_AREA_FILE_MAPPING: dict[Resolution, Path] = {
    "10m": STATIC_DIR / "admin_areas" / "admin-areas_10m.geojson.gz",
    "50m": STATIC_DIR / "admin_areas" / "admin-areas_50m.geojson.gz",
    "110m": STATIC_DIR / "admin_areas" / "admin-areas_110m.geojson.gz",
}
GEOJSON_ADMIN_KEY = "adm0_a3"

# Checks
# Ensure data dirs exists
for _d in [DATA_DIR, BM_DATA_DIR, LJ_DATA_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

# Ensure bearer token is set
if not BM_TOKEN or len(BM_TOKEN) == 0:
    print("Bearer token not set. Please set the BLACKMARBLE_TOKEN environment variable", file=sys.stderr)
    sys.exit(1)
