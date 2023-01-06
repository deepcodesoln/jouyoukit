from libjyk import jykdb
from libjyk.query import (
    KANJI_GRADES,
    SUPPORTED_SORT,
    get_kanji,
    get_kanji_for_grade,
    get_radicals_for_grade,
    get_radicals_unique_to_grade,
    get_radicals_introduced_in_grade,
    TableDoesNotExist,
)
from libjyk.format import (
    SUPPORTED_FORMATS,
    kanji_csv_header,
    kanji_list_to_csv,
    radical_csv_header,
    radical_list_to_csv,
)


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
        "--get-kanji-for-grade",
        metavar="grade",
        type=int,
        choices=KANJI_GRADES,
        # `choices` is not present in help text for items in mutually exclusive groups,
        # so we add it here.
        help=f"Get all kanji of a specific grade; choices: {KANJI_GRADES}",
    )
    actions.add_argument(
        "--get-radicals-for-grade",
        metavar="grade",
        type=int,
        choices=KANJI_GRADES,
        # Add `choices` in help text as we do for `--get-kanji-for-grade`.
        help=f"Get all radicals used in a specific grade; choices: {KANJI_GRADES}",
    )
    actions.add_argument(
        "--get-radicals-unique-to-grade",
        metavar="grade",
        type=int,
        choices=KANJI_GRADES,
        # Add `choices` in help text as we do for `--get-kanji-for-grade`.
        help=f"Get all radicals unique to a specific grade; choices: {KANJI_GRADES}",
    )
    actions.add_argument(
        "--get-radicals-introduced-in-grade",
        metavar="grade",
        type=int,
        choices=KANJI_GRADES,
        # Add `choices` in help text as we do for `--get-kanji-for-grade`.
        help=(
            "Get all radicals new to some grade relative to all grades before; "
            + f"choices: {KANJI_GRADES}"
        ),
    )
    actions.add_argument(
        "--print-kanji-csv-header",
        action="store_true",
        help="Print the column headers for kanji represented as CSV",
    )
    actions.add_argument(
        "--print-radical-csv-header",
        action="store_true",
        help="Print the column headers for radicals represented as CSV",
    )
    parser.add_argument(
        "--sort-by",
        choices=SUPPORTED_SORT,
        help="The kanji property to sort by for kanji queries that return more than 1 result",
    )
    parser.add_argument(
        "--format-as",
        choices=SUPPORTED_FORMATS,
        help="Convert particular tool output to a particular format",
    )

    parser.set_defaults(func=_main)


def _main(args) -> int:
    """
    :return: A typical program exit status code.
    :rtype: int
    """
    try:
        if args.build:
            jykdb.build(args.build)
        elif args.query_kanji:
            kanji = get_kanji(args.query_kanji)
            out = kanji_list_to_csv([kanji]) if args.format_as == "csv" else kanji
            print(out)
        elif args.get_kanji_for_grade:
            kanji = get_kanji_for_grade(args.get_kanji_for_grade, args.sort_by)
            if args.format_as == "csv":
                out = kanji_list_to_csv(kanji)
                print(out)
            else:
                for k in kanji:
                    print(k)
        elif args.get_radicals_for_grade:
            radicals = get_radicals_for_grade(args.get_radicals_for_grade, args.sort_by)
            if args.format_as == "csv":
                out = radical_list_to_csv(radicals)
                print(out)
            else:
                for r in radicals:
                    print(r)
        elif args.get_radicals_unique_to_grade:
            radicals = get_radicals_unique_to_grade(
                args.get_radicals_unique_to_grade, args.sort_by
            )
            if args.format_as == "csv":
                out = radical_list_to_csv(radicals)
                print(out)
            else:
                for r in radicals:
                    print(r)
        elif args.get_radicals_introduced_in_grade:
            radicals = get_radicals_introduced_in_grade(
                args.get_radicals_introduced_in_grade, args.sort_by
            )
            if args.format_as == "csv":
                out = radical_list_to_csv(radicals)
                print(out)
            else:
                for r in radicals:
                    print(r)
        elif args.print_kanji_csv_header:
            print(kanji_csv_header())
        elif args.print_radical_csv_header:
            print(radical_csv_header())
    except TableDoesNotExist:
        print("The jouyou toolkit database does not exist. Try `jyk.py db --build`.")
        return 1

    return 0
