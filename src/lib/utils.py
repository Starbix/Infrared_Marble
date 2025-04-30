import os
import sys
from pathlib import Path

from blackmarble.types import Product

# Note: This code runs whenever the module is first imported.
# This is to make sure that the DATA_DIR and BEARER_TOKEN variables are appropriately set.

PROJECT_ROOT = Path(__file__).parents[2]
STATIC_DIR = PROJECT_ROOT / 'static'

# Directory to download files to (ignore in git)
if _data_dir_from_env := os.getenv("DATA_DIR"):
    DATA_DIR = Path(_data_dir_from_env)
else:
    DATA_DIR = PROJECT_ROOT / "data"

# Derived constants
BM_DATA_DIR = DATA_DIR / "blackmarble"
LJ_DATA_DIR = DATA_DIR / "luojia"

# Ensure data dirs exists
for _d in [DATA_DIR, BM_DATA_DIR, LJ_DATA_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

# Get Bearer token from environment
_bearer_token_from_env = os.getenv("BLACKMARBLE_TOKEN")

if not _bearer_token_from_env or len(_bearer_token_from_env) == 0:
    print(
        "Bearer token not set. Please set the BLACKMARBLE_TOKEN environment variable",
        file=sys.stderr,
    )
    sys.exit(1)

BEARER_TOKEN = _bearer_token_from_env

_bm_product = os.environ.get("BM_PRODUCT")
BM_PRODUCT: Product = Product[_bm_product] if _bm_product else Product.VNP46A2
BM_VARIABLE: str | None = os.environ.get("BM_VARIABLE")  # Default varible for product
_bm_quality_flag = os.environ.get("BM_QUALITY_FLAG")
BM_QUALITY_FLAG: list[int] = [int(x) for x in _bm_quality_flag.split(",")] if _bm_quality_flag else []


DEFAULT_DATES_FILE = STATIC_DIR / "dates_luojia_myanmar.csv"
DEFAULT_GDF_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_MMR_1.json.zip"
DEFAULT_LJ_IDS_FILE = STATIC_DIR / "luojia_image_ids.csv"

ALL_ADMIN_AREAS_GEOJSON_FILE = STATIC_DIR / 'countries.geo.json.gz'

def get_default_variable_for_product(product: Product):
    if product == Product.VNP46A1:
        return "DNB_At_Sensor_Radiance_500m"
    if product == Product.VNP46A2:
        return "Gap_Filled_DNB_BRDF-Corrected_NTL"
    if product == Product.VNP46A3:
        return "NearNadir_Composite_Snow_Free"
    if product == Product.VNP46A4:
        return "NearNadir_Composite_Snow_Free"
