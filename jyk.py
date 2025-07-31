import argparse

from jouyoukit.jyk import build_db, db_to_csv


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    db_builder = subparsers.add_parser(
        "build_db", help="Extract jouyou kanji and vocabulary into a local JSON dictionary"
    )
    db_builder.add_argument("kanjidic2", help="A Kanjidic2 XML database.")
    db_builder.add_argument("jmdict", help="A JMdict XML database.")
    db_builder.set_defaults(func=build_db)

    csv_builder = subparsers.add_parser(
        "db_to_csv", help="Convert a local JSON dictionary into CSV files by level"
    )
    csv_builder.set_defaults(func=db_to_csv)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
