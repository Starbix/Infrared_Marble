import argparse
import sys
from pathlib import Path

from download import fetch_gdf, get_dates
from utils import DEFAULT_DATES_FILE, DEFAULT_GDF_URL


def handle_bm_commands(args: argparse.Namespace):
    if args.bm_command == "download":
        from download import bm_dataset_preprocess

        if args.file:
            dates = get_dates(args.file)
        else:
            dates = args.dates
        print("Selected GDF:    ", args.gdf.split("/")[-1])
        gdf = fetch_gdf(args.gdf, force=args.force)
        print("Selected dates:", ", ".join(d.isoformat() for d in dates))
        bm_dataset_preprocess(gdf=gdf, dates=dates, force=args.force)
        print("Download done.")


def main():
    # Main argument parser
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(dest="command")

    # Blackmarble parser
    bm_parser = subparsers.add_parser("bm", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    bm_subparsers = bm_parser.add_subparsers(dest="bm_command")

    bm_download_parser = bm_subparsers.add_parser(
        "download", formatter_class=argparse.ArgumentDefaultsHelpFormatter
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
        "-g", "--gdf", default=DEFAULT_GDF_URL, help="URL to the GDF JSON file"
    )
    bm_download_parser.add_argument(
        "--force", action="store_true", help="Force re-downloading and processing of files"
    )

    # ... Add more subparsers here

    # General options
    parser.add_argument("-v", "--verbose", action="store_true", help="More verbose logging")

    # Main program
    args = parser.parse_args()

    try:
        if args.command == "bm":
            handle_bm_commands(args)

        # ... Add more subcommands here
    except Exception as e:
        if args.verbose:
            raise e
        else:
            print(str(e), file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
