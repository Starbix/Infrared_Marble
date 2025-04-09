import datetime
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from concurrent.futures import ThreadPoolExecutor

from matplotlib import pyplot as plt

from lib.download import bm_dataset_preprocess, fetch_gdf, get_dates
from lib.loading import get_bm
from lib.utils import DEFAULT_DATES_FILE, DEFAULT_GDF_URL
from lib.visualization import plot_daily_radiance


def setup_bm_parser(parser: ArgumentParser, parents: list[ArgumentParser]):
    bm_parent = ArgumentParser(add_help=False)
    bm_parent.add_argument("-g", "--gdf", default=DEFAULT_GDF_URL, help="URL to the GDF JSON file")

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
    bm_download_parser.add_argument(
        "-d", "--dates", nargs="+", help="Manually list dates to download in ISO format"
    )
    bm_download_parser.add_argument(
        "--force", action="store_true", help="Force re-downloading and processing of files"
    )

    # Visualize
    bm_show_parser = subparsers_bm.add_parser(
        "show",
        add_help=False,
        parents=parents + [bm_parent],
        formatter_class=ArgumentDefaultsHelpFormatter,
        help="Visualize data in the Blackmarble dataset",
    )
    bm_show_parser.add_argument("dates", nargs="+", help="Date(s) to visualize")


def handle_bm_commands(args: Namespace):
    if args.bm_command == "download":
        if args.file:
            dates = get_dates(args.file)
        else:
            dates = args.dates
        print("Selected GDF:    ", args.gdf.split("/")[-1])
        gdf = fetch_gdf(args.gdf, force=args.force)
        print("Selected dates:", ", ".join(d.isoformat() for d in dates))
        bm_dataset_preprocess(gdf=gdf, dates=dates, force=args.force)
        print("Download done.")

    if args.bm_command == "show":
        gdf = fetch_gdf(args.gdf)
        raster = get_bm()

        # Show all figures in parallel
        dates = [datetime.date.fromisoformat(d) for d in args.dates]

        for date in dates:
            figure = plot_daily_radiance(gdf, raster, date)

        plt.show(block=True)
