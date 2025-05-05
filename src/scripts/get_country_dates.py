from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
import gzip
import logging
import os
import geopandas
import pandas as pd
import xml.etree.ElementTree as ET

from rasterio import CRS
from shapely.geometry import Polygon
from lib.utils import ADMIN_AREA_FILE_MAPPING, DATA_DIR, STATIC_DIR
from tqdm import tqdm

logging.basicConfig(level=logging.DEBUG)


def process_country(tile_index: pd.DataFrame, crs: CRS, country: pd.Series, gdf_country: geopandas.GeoDataFrame):
    results = []
    for _, tile in tile_index.iterrows():
        geotiff_polygon = Polygon(
            [
                (tile["lt"][0], tile["lt"][1]),
                (tile["rt"][0], tile["rt"][1]),
                (tile["rb"][0], tile["rb"][1]),
                (tile["lb"][0], tile["lb"][1]),
            ]
        )
        geotiff_geoseries = geopandas.GeoSeries([geotiff_polygon], crs=crs)
        intersection = gdf_country.intersects(geotiff_geoseries.union_all())
        if intersection.any():
            logging.debug("Found intersection for country %s: %s, %s", country.adm0_a3, tile.date, tile.tile_name)
            results.append([country.adm0_a3, tile.date, tile.tile_name])
    return country.adm0_a3, results


def main():
    META_DIR = DATA_DIR / "luojia" / "metadata"

    dates = set()
    data = []

    print("Building Tile Index...")
    for path in tqdm(list(META_DIR.iterdir()), desc="Reading meta files..."):
        tree = ET.parse(path)
        root = tree.getroot()
        # Extract the date part of imaging time
        imaging_time = tree.find(".//imagingTime").text.split("T")[0]
        imaging_date = datetime.strptime(imaging_time, "%Y-%m-%d").date()
        lt = (float(tree.find(".//LTLongitude").text), float(tree.find(".//LTLatitude").text))
        rt = (float(tree.find(".//RTLongitude").text), float(tree.find(".//RTLatitude").text))
        rb = (float(tree.find(".//RBLongitude").text), float(tree.find(".//RBLatitude").text))
        lb = (float(tree.find(".//LBLongitude").text), float(tree.find(".//LBLatitude").text))
        dates.add(imaging_date)
        data.append([imaging_date, path.stem.replace("_meta", ""), lt, rt, rb, lb])

    all_dates = pd.DataFrame({"date": sorted(list(dates))})
    all_dates.to_csv(STATIC_DIR / "all_dates.csv", index=False)

    tile_index = pd.DataFrame(data, columns=["date", "tile_name", "lt", "rt", "rb", "lb"])
    tile_index.to_csv(STATIC_DIR / "tile_index.csv.gz", index=False, compression="gzip")

    with gzip.open(ADMIN_AREA_FILE_MAPPING["110m"], "rt") as f:
        gdf = geopandas.read_file(f)

    max_workers = (os.cpu_count() or 4) - 2
    results_combined = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        print("Finding available dates per country.")
        print(f"Using Process Pool Executor with {max_workers} workers.")
        try:
            futures = [
                executor.submit(
                    process_country, tile_index=tile_index, crs=gdf.crs, country=country, gdf_country=gdf.iloc[[idx]]
                )
                for idx, country in gdf.iterrows()
            ]

            for future in (pb := tqdm(as_completed(futures), total=len(futures), desc="Processing countries...")):
                admin_id, results = future.result()
                pb.write(f"Found {len(results)} tiles for country {admin_id}")
                results_combined.extend(results)
        except KeyboardInterrupt:
            executor.shutdown(cancel_futures=True)

    country_meta = pd.DataFrame(results_combined, columns=["country", "date", "tile_name"])
    country_meta.to_csv(STATIC_DIR / "country_meta.csv.gz", index=False, compression="gzip")


if __name__ == "__main__":
    main()
