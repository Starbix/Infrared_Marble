import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from cli.blackmarble import handle_bm_commands, setup_bm_parser
from cli.get import handle_get_commands, setup_get_parser
from cli.luojia import handle_lj_commands, setup_lj_parser


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
        parents=[root_parent],
        add_help=False,
        formatter_class=ArgumentDefaultsHelpFormatter,
        help="Commands relating to the Luojia dataset",
    )
    setup_lj_parser(parser_lj, parents=[root_parent])

    # Miscellaneous get parser
    parser_get = subparsers.add_parser(
        "get",
        parents=[root_parent],
        add_help=False,
        formatter_class=ArgumentDefaultsHelpFormatter,
        help="List/get resources",
    )
    setup_get_parser(parser_get, parents=[root_parent])

    # ... Add more subparsers here

    # Main program
    args = parser.parse_args()

    try:
        if args.command == "bm":
            handle_bm_commands(args)
        elif args.command == "lj":
            handle_lj_commands(args)
        elif args.command == "get":
            handle_get_commands(args)

        # ... Add more subcommands here
    except Exception as e:
        if args.verbose:
            raise e
        else:
            print(str(e), file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
