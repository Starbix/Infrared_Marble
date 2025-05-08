from datetime import date, datetime, time, timedelta
from pathlib import Path

import pandas as pd
import requests

from lib.constants import DEFAULT_DATES_FILE
from lib.download import get_dates


def list_dates(file: str | Path | None = None):
    file = Path(file) if file else DEFAULT_DATES_FILE

    if not file.exists():
        raise ValueError(f"File does not exist: {file}")

    dates = get_dates(file)

    return dates


def get_day_cloud_coverage(date_str: str, location: str = None):
    API_KEY = "C6FNLY48VY2CHXVP2TD9534X4"

    luojia_time = datetime.combine(date.fromisoformat(date_str), time(22, 0)).isoformat()
    bm_time = datetime.combine(date.fromisoformat(date_str) + timedelta(days=1), time(1, 0)).isoformat()

    req_string = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{luojia_time}?unitGroup=metric&include=current&key={API_KEY}&contentType=json"
    response = requests.request("GET", req_string)
    luojia_data = response.json()

    date_str = (date.fromisoformat(date_str) + timedelta(days=1)).isoformat()
    req_string = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{bm_time}?unitGroup=metric&include=current&key={API_KEY}&contentType=json"
    response = requests.request("GET", req_string)
    bm_data = response.json()

    luojia_cloud_coverage = None
    bm_cloud_coverage = None

    luojia_cloud_coverage = luojia_data["currentConditions"]["cloudcover"]
    bm_cloud_coverage = bm_data["currentConditions"]["cloudcover"]

    if luojia_cloud_coverage is None or bm_cloud_coverage is None:
        raise ValueError("Could not find cloud coverage data for given time")

    return luojia_cloud_coverage, bm_cloud_coverage


def add_cloud_coverage(file: str | Path, location: str = None):
    file = Path(file)

    if not file.exists():
        raise ValueError(f"File does not exist: {file}")

    df = pd.read_csv(file)

    for i, row in df.iterrows():
        luojia_cloud, bm_cloud = get_day_cloud_coverage(row["date"], location)
        df.at[i, "luojia_cloud"] = luojia_cloud
        df.at[i, "bm_cloud"] = bm_cloud

    df.to_csv(file, index=False)


def sort_by_cloud_coverage(file: str | Path, location: str = None):
    file = Path(file)

    data = []

    if not file.exists():
        raise ValueError(f"File does not exist: {file}")

    df = pd.read_csv(file)
    dates = df["date"].tolist()

    for date in dates:
        luojia_cloud, bm_cloud = get_day_cloud_coverage(date, location)
        data.append((date, luojia_cloud, bm_cloud))

    return sorted(data, key=lambda tup: (tup[1] + tup[2]) / 2)
