"""This module contains items related to the jouyou toolkit's databases."""

JOUYOU_TABLE_NAME = "jouyou"


"""
The schema for a row in the jouyou table. The columns follow the order of names in
JOUYOU_TABLE_ROW_NAMES. The bytes columns are pickle-serialized data.
"""
JOUYOU_TABLE_ROW_SCHEMA = tuple[str, str, bytes, bytes, bytes, int, int]


"""The names of each column of a row in JOUYOU_TABLE_NAME."""
JOUYOU_TABLE_ROW_NAMES = [
    "kanji",
    "radical",
    "onyomi",
    "kunyomi",
    "meanings",
    "grade",
    "frequency",
]
