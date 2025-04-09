import datetime
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace, _SubParsersAction

from matplotlib import pyplot as plt
from matplotlib.pylab import pareto

from download import fetch_gdf, get_dates
from utils import DEFAULT_DATES_FILE, DEFAULT_GDF_URL
from visualization import plot_daily_radiance


def handle_bm_commands(args: Namespace):
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

    if args.bm_command == "show":
        from download import bm_dataset_preprocess

        gdf = fetch_gdf(args.gdf)
        date = datetime.date.fromisoformat(args.date)
        raster = bm_dataset_preprocess(gdf=gdf, dates=[date])
        figure = plot_daily_radiance(gdf, raster, date)
        plt.show(block=True)


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
    bm_show_parser.add_argument("date", help="Date to visualize")


def setup_lj_parser(parser: ArgumentParser, parents: list[ArgumentParser]):
    pass


def main():
    # Root parent parser
    root_parent = ArgumentParser()
    root_parent.add_argument(
        "-v", "--verbose", action="store_true", help="Print debugging information"
    )

    # Main argument parser
    parser = ArgumentParser(
        description="NTL Tool", prog="ntl-tool", formatter_class=ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command", help="Subcommand to run")

    # Blackmarble parser
    parser_bm = subparsers.add_parser(
        "bm",
        parents=[root_parent],
        add_help=False,
        formatter_class=ArgumentDefaultsHelpFormatter,
        help="Commands relating to the Blackmarble dataset",
    )
    setup_bm_parser(parser_bm, parents=[root_parent])

    # Luojia parser
    parser_lj = subparsers.add_parser(
        "lj",
        parents=[parser],
        add_help=False,
        formatter_class=ArgumentDefaultsHelpFormatter,
        help="Commands relating to the Luojia dataset",
    )
    setup_lj_parser(parser_lj, parents=[root_parent])

    # ... Add more subparsers here

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
