# %%

from api.helpers import get_admin_area_by_id
from lib.utils import ADMIN_AREA_FILE_MAPPING


admin_area = get_admin_area_by_id("GRC")

admin_area
# %%

import geopandas
import gzip

with gzip.open(ADMIN_AREA_FILE_MAPPING["50m"], "rt", encoding="utf-8") as f:
    gdf = geopandas.read_file(f)

gdf[gdf["adm0_a3"] == "GRC"]
# %%

gdf.to_crs("EPSG:4326").dissolve()
# %%
gdf.geometry
