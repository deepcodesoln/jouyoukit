import argparse


from db.db import extend_args as db_extend_args


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    db_extend_args(subparsers)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
