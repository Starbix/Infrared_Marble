import os
import sys
from pathlib import Path

from blackmarble.types import Product

# Note: This code runs whenever the module is first imported.
# This is to make sure that the DATA_DIR and BEARER_TOKEN variables are appropriately set.

PROJECT_ROOT = Path(__file__).parents[2]

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

BM_PRODUCT = Product.VNP46A2
BM_VARIABLE = None  # Default varible for product
BM_QUALITY_FLAG = [2]  # Drop low-quality pixels

DEFAULT_DATES_FILE = PROJECT_ROOT / "dates_luojia_myanmar.csv"
DEFAULT_GDF_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_MMR_1.json.zip"
DEFAULT_LJ_IDS_FILE = PROJECT_ROOT / "luojia_image_ids.csv"
