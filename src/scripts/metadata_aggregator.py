#!/usr/bin/env python3
"""
metadata_aggregator.py

Scan a fixed directory of XML metadata files, extract imaging date & country for each,
aggregate counts per (date, country), and:

  • Return the results as a list of (date, country, count) tuples
  • Write those results to data/luojia/image_counts.csv

Usage:
    python metadata_aggregator.py

Dependencies:
    pip install reverse_geocoder pycountry tqdm
"""

import csv
import os
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import pycountry
import reverse_geocoder as rg
from tqdm import tqdm  # Progress bar

from lib.constants import LJ_DATA_DIR, STATIC_DIR

# === Paths (change only if your layout differs) ===
METADATA_DIR = LJ_DATA_DIR / "metadata"
OUTPUT_CSV = STATIC_DIR / "image_counts.csv"


def get_country_from_coords(lat: float, lon: float) -> str:
    """
    Reverse-geocode (lat, lon) to a country name using offline data.
    Returns the full country name if available, otherwise the ISO alpha-2 code.
    """
    result = rg.search((lat, lon), mode=2)
    cc = result[0]["cc"]  # e.g. "CN", "US"
    country = pycountry.countries.get(alpha_2=cc)
    return country.name if country else cc


def parse_metadata_file(xml_path: str) -> Tuple[str, str]:
    """
    Parse one XML metadata file and return (date_str, country_name).

    - date_str: acquisition date in "YYYY-MM-DD" (UTC)
    - country_name: full country name for the image center.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Find the ProductInfo block
    prod = root.find("ProductInfo")
    if prod is None:
        raise ValueError("Missing <ProductInfo>")

    # 1) Extract & parse imagingTime
    t = prod.findtext("imagingTime")
    if not t:
        raise ValueError("Missing <imagingTime>")
    try:
        dt = datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        dt = datetime.strptime(t, "%Y-%m-%dT%H:%M:%S")
    date_str = dt.date().isoformat()

    # 2) Extract center coords
    lat_text = prod.findtext("CenterLatitude")
    lon_text = prod.findtext("CenterLongitude")
    if lat_text is None or lon_text is None:
        raise ValueError("Missing center coordinates")
    lat, lon = float(lat_text), float(lon_text)

    # 3) Reverse-geocode to country
    country = get_country_from_coords(lat, lon)
    return date_str, country


def parse_metadata_file_wrapper(xml_path, fname):
    try:
        date_str, country = parse_metadata_file(xml_path)
    except Exception as e:
        print(f"Warning: skipping {fname!r}: {e}", file=sys.stderr)
        return None, None
    return date_str, country


def aggregate_image_counts() -> List[Tuple[str, str, int]]:
    """
    Scan all .xml files in METADATA_DIR, count images per (date, country),
    and return a sorted list of (date, country, count).
    """
    # 1) List all XML files so tqdm knows the total
    all_files = [fname for fname in os.listdir(METADATA_DIR) if fname.lower().endswith(".xml")]

    counts: dict[Tuple[str, str], int] = {}

    # 2) Process with a progress bar

    # Parallel process all file names
    with ThreadPoolExecutor() as executor:
        try:
            futures = [
                executor.submit(parse_metadata_file_wrapper, os.path.join(METADATA_DIR, fname), fname)
                for fname in all_files
            ]
            for future in tqdm(as_completed(futures), desc="Scanning metadata", unit="file", total=len(all_files)):
                date_str, country = future.result()
                if date_str is None or country is None:
                    continue
                key = (date_str, country)
                counts[key] = counts.get(key, 0) + 1
        except KeyboardInterrupt:
            executor.shutdown(wait=False, cancel_futures=True)

    # 3) Build & sort result list
    results = [(d, c, cnt) for (d, c), cnt in counts.items()]
    results.sort(key=lambda row: (row[0], row[1]))
    return results


def save_to_csv(rows: List[Tuple[str, str, int]], csv_path: str | Path) -> None:
    """
    Write the list of (date, country, count) into a CSV file.
    Overwrites any existing file at csv_path.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Country", "Count"])
        for date, country, cnt in rows:
            writer.writerow([date, country, cnt])


def main():
    # 1) Ensure metadata dir exists
    if not os.path.isdir(METADATA_DIR):
        print(f"Error: metadata directory not found:\n  {METADATA_DIR}", file=sys.stderr)
        sys.exit(1)

    # 2) Aggregate into memory
    table = aggregate_image_counts()

    # 3) Persist to CSV
    save_to_csv(table, OUTPUT_CSV)
    print(f"✔ Wrote {len(table)} rows to:\n    {OUTPUT_CSV}")

    # 4) (Optional) also print a preview
    print("\nFirst 5 entries:")
    for row in table[:5]:
        print(f"  {row[0]:10} | {row[1]:20} | {row[2]}")

    # If you need the array in code, just call aggregate_image_counts()
    # and use the returned list `table` directly.


if __name__ == "__main__":
    main()
