from db.build import build


def extend_args(subparsers):
    parser = subparsers.add_parser(
        "db", help="Jouyou kanji database-related functionality"
    )

    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument(
        "--build",
        metavar="kanjidic2_file",
        help="Build a local, persistent database from a kanjidic2 XML file",
    )

    parser.set_defaults(func=main)


def main(args):
    if args.build:
        build(args.build)
