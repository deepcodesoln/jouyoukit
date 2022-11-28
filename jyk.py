import argparse
import sys


from db.main import extend_args as db_extend_args


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    db_extend_args(subparsers)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    retcode = main()
    if retcode:
        sys.exit(retcode)
