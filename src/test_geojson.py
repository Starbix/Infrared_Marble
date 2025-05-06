# %%

import geopandas

from lib.utils import DATA_DIR

with open(DATA_DIR / "countries.geojson") as f:
    gdf = geopandas.read_file(f)

gdf


# %%

gdf.columns
