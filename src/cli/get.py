import os
from argparse import ArgumentParser, Namespace
from os import isatty
from pathlib import Path

import numpy as np
from tabulate import tabulate

from lib.admin_areas import dates_from_csv
from lib.bm import bm_load_from_zarr
from lib.config import DEFAULT_DATES_FILE, DEFAULT_GDF_FILE


def setup_get_parser(parser: ArgumentParser, parents: list[ArgumentParser]):
    parser.add_argument("resource", choices=["dates"], help="Resource to get")
    parser.add_argument(
        "-f",
        "--file",
        default=DEFAULT_DATES_FILE,
        help="Input file with dates, one date per line, ISO format",
    )
    parser.add_argument("-g", "--gdf", default=DEFAULT_GDF_FILE, help="URL to the GDF JSON file")


def handle_get_commands(args: Namespace):
    res = args.resource
    if res == "dates":
        dates = dates_from_csv(filename=args.file)
        raster = bm_load_from_zarr()
        if isatty(1):
            print(f"Source: {Path(args.file).relative_to(os.getcwd())}")
            print("---")
            print(
                tabulate(
                    [
                        (
                            date.isoformat(),
                            "Yes" if np.datetime64(date) in raster.time else "No",
                            "n/a",
                        )
                        for date in dates
                    ],
                    headers=("Date", "Downloaded (BM)", "Downloaded (LJ)"),
                )
            )
        else:
            print("\n".join(d.isoformat() for d in dates))
