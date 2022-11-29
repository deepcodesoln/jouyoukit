from libjyk.database.build import build
from libjyk.database.database import TableDoesNotExist
from libjyk.database.transact import KANJI_GRADES, get_kanji, get_kanji_by_grade


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
    # TODO(orphen) Generalize query CLI: one command, various filters.
    actions.add_argument(
        "--get-kanji-by-grade",
        metavar="grade",
        type=int,
        choices=KANJI_GRADES,
        # `choices` is not present in help text for items in mutually exclusive groups,
        # so we add it here.
        help=f"Search the database for all kanji of a specific grade; choices: {KANJI_GRADES}",
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
