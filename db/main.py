from libjyk.jykdb.build import build
from libjyk.query import (
    KANJI_GRADES,
    SUPPORTED_SORT,
    get_kanji,
    get_kanji_by_grade,
    TableDoesNotExist,
)
from libjyk.format import SUPPORTED_FORMATS, kanji_list_to_csv, radical_list_to_csv


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
    actions.add_argument(
        "--get-radicals-for-level",
        metavar="level",
        type=int,
        choices=KANJI_GRADES,
        # Add `choices` in help text as we do for `--get-kanji-by-grade`.
        help="Get all unique radicals for all kanji by grade; choices: {KANJI_CHOICES}",
    )

    parser.add_argument(
        "--sort-by",
        choices=SUPPORTED_SORT,
        help="The kanji property to sort by for queries that return more than 1 result",
    )
    parser.add_argument(
        "--format-as",
        choices=SUPPORTED_FORMATS,
        help="Convert tool output to a particular format",
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
            kanji = get_kanji(args.query_kanji)
            out = kanji_list_to_csv([kanji]) if args.format_as == "csv" else kanji
            print(out)
        elif args.get_kanji_by_grade:
            kanji = get_kanji_by_grade(args.get_kanji_by_grade, args.sort_by)
            if args.format_as == "csv":
                out = kanji_list_to_csv(kanji)
                print(out)
            else:
                for k in kanji:
                    print(k)
        elif args.get_radicals_for_level:
            # TODO(orphen) Move this functionality into libjyk.
            # As we cannot search the database for radicals directly, we have to
            # operate on the list of all kanji for a specific grade.
            kanji = get_kanji_by_grade(args.get_unique_radicals_for_level, args.sort_by)
            radicals = set()
            for k in kanji:
                radicals.add(k.radical)
            if args.format_as == "csv":
                out = radical_list_to_csv(list(radicals))
                print(out)
            else:
                for r in radicals:
                    print(r)
    except TableDoesNotExist:
        print("The jouyou toolkit database does not exist. Try `jyk.py db --build`.")
        return 1

    return 0
