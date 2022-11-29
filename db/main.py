from db.build import build
from db.transact import get_kanji, get_kanji_by_grade
from libjyk.database import TableDoesNotExist


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
    actions.add_argument(
        "--query-kanji",
        metavar="kanji",
        help="Search the database for a specific kanji",
    )
    actions.add_argument(
        "--get-kanji-by-grade",
        metavar="grade",
        type=int,
        help="Search the database for all kanji of a specific grade",
    )

    parser.set_defaults(func=_main)


def _main(args) -> int:
    """
    :return: A typical program exit status code.
    :rtype: int
    """
    try:
        if args.build:
            build(args.build)
        elif args.query_kanji:
            print(get_kanji(args.query_kanji))
        elif args.get_kanji_by_grade:
            for kanji in get_kanji_by_grade(args.get_kanji_by_grade):
                print(kanji)
    except TableDoesNotExist:
        print("The jouyou toolkit database does not exist. Try `jyk.py db --build`.")
        return 1

    return 0
