import os
import sys
from pathlib import Path

# Note: This code runs whenever the module is first imported.
# This is to make sure that the DATA_DIR and BEARER_TOKEN variables are appropriately set.

# Directory to download files to (ignore in git)
if _data_dir_from_env := os.getenv("DATA_DIR"):
    DATA_DIR = Path(_data_dir_from_env)
else:
    DATA_DIR = Path(__file__).parents[1] / "data"

# Derived constants
BM_DATA_DIR = DATA_DIR / "blackmarble"
LUOJIA_DATA_DIR = DATA_DIR / "luojia"

# Ensure data dirs exists
for _d in [DATA_DIR, BM_DATA_DIR, LUOJIA_DATA_DIR]:
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


DEFAULT_DATES_FILE = Path(__file__).parents[1] / "dates_luojia_myanmar.csv"
DEFAULT_GDF_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_MMR_1.json.zip"
