import datetime
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace

import geopandas
from matplotlib import pyplot as plt

from lib.admin_areas import dates_from_csv
from lib.bm import bm_load_from_zarr, bm_store_to_zarr
from lib.config import DEFAULT_DATES_FILE, DEFAULT_GDF_FILE
from lib.visualization import plot_daily_radiance, plot_difference, plot_series


def setup_bm_parser(parser: ArgumentParser, parents: list[ArgumentParser]):
    bm_parent = ArgumentParser(add_help=False)
    bm_parent.add_argument("-g", "--gdf", default=DEFAULT_GDF_FILE, help="URL to the GDF JSON file")

    subparsers_bm = parser.add_subparsers(dest="bm_command")

    # Download
    bm_download_parser = subparsers_bm.add_parser(
        "download",
        add_help=False,
        parents=parents + [bm_parent],
        formatter_class=ArgumentDefaultsHelpFormatter,
        help="Download the Blackmarble dataset locally",
    )
    bm_download_parser.add_argument(
        "-f",
        "--file",
        default=DEFAULT_DATES_FILE,
        help="Input file with dates, one date per line, ISO format",
    )
    bm_download_parser.add_argument("-d", "--dates", nargs="+", help="Manually list dates to download in ISO format")
    bm_download_parser.add_argument("--force", action="store_true", help="Force re-downloading and processing of files")

    # Visualize
    bm_show_parser = subparsers_bm.add_parser(
        "show",
        add_help=False,
        parents=parents + [bm_parent],
        formatter_class=ArgumentDefaultsHelpFormatter,
        help="Visualize data in the Blackmarble dataset",
    )
    bm_show_parser.add_argument("dates", nargs="*", help="Date(s) to visualize")
    bm_show_parser.add_argument(
        "-f",
        "--file",
        help="Input file with dates, one date per line, ISO format",
    )
    bm_show_parser.add_argument("--diff", action="store_true", help="Show difference in radiance between two dates")
    bm_show_parser.add_argument(
        "--time-series",
        action="store_true",
        help="Show time series of mean daily radiance over provided dates",
    )


def handle_bm_commands(args: Namespace):
    if args.bm_command == "download":
        if args.file:
            dates = dates_from_csv(args.file)
        else:
            dates = args.dates
        print("Selected GDF:    ", args.gdf.split("/")[-1])
        gdf = geopandas.read_file(args.gdf, force=args.force)
        print("Selected dates:", ", ".join(dates))
        bm_store_to_zarr(gdf=gdf, dates=[datetime.date.fromisoformat(d) for d in dates], force=args.force)
        print("Download done.")

    if args.bm_command == "show":
        gdf = geopandas.read_file(args.gdf)
        raster = bm_load_from_zarr()
        dates: list[str] = args.dates
        if args.file:
            dates = dates_from_csv(args.file)

        if args.diff:
            # Show difference between two dates
            assert len(dates) == 2, "When using --diff option, must provide exactly two dates"
            plot_difference(gdf, raster, date1=dates[0], date2=dates[1])
        if args.time_series:
            plot_series(raster, dates)
        else:
            # Default: Plot radiance
            # Show all figures in parallel
            for date in dates:
                plot_daily_radiance(gdf, raster, date)

        plt.show(block=True)
