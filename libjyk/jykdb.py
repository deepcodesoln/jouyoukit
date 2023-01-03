"""This module contains code to build the persistent libjyk jouyou kanji database."""

import os
import pickle
import sqlite3
from typing import Optional

from libjyk.kanji import JOUYOU_KANJI
from libjyk.kanji import Kanji
from libjyk.parser.kanjidic2 import parse_kanjidic2
from libjyk.pathing import JYK_USER_DIR, create_persistent_jyk_paths
from libjyk.radicals import KANGXI_RADICALS


JYK_DEFAULT_DB = os.path.expanduser(os.path.join(JYK_USER_DIR, "jyk.db"))
JOUYOU_TABLE_NAME = "jouyou"

"""
The schema for a row in the jouyou table. The columns follow the order of names in
JOUYOU_TABLE_ROW_NAMES. The bytes columns are pickle-serialized data.
"""
JOUYOU_TABLE_ROW_SCHEMA = tuple[str, int, bytes, bytes, bytes, int, int]

"""The names of each column of a row in JOUYOU_TABLE_NAME."""
JOUYOU_TABLE_ROW_NAMES = [
    "kanji",
    # TODO(orphen) Update this to `kangxi_radical_id`.
    "kangxi_radical",
    "onyomi",
    "kunyomi",
    "meanings",
    "grade",
    "frequency",
]


def _kanji_to_row(kanji: Kanji) -> JOUYOU_TABLE_ROW_SCHEMA:
    """
    :param kanji: An instance of Kanji to transform into a jouyou database row.
    :type kanji: Kanji
    :return: A tuple containing the fields of a Kanji instance. This tuple can be
        written directly into a jouyou toolkit kanji database. Fields that cannot be
        stored directly in the database are first serialized and can then be stored as
        BLOBs.
    :rtype: JOUYOU_TABLE_ROW_SCHEMA
    """
    return (
        kanji.kanji,
        kanji.radical.number,
        pickle.dumps(kanji.onyomi, fix_imports=False),
        pickle.dumps(kanji.kunyomi, fix_imports=False),
        pickle.dumps(kanji.meanings, fix_imports=False),
        kanji.grade,
        kanji.frequency,
    )


def row_to_kanji(row: JOUYOU_TABLE_ROW_SCHEMA) -> Kanji:
    """
    :param row: A row from JOUYOU_TABLE_NAME.
    :type row: JOUYOU_TABLE_KANJI_SCHEMA.
    :return: The database row represented as a Kanji instance.
    :rtype: Kanji
    """
    return Kanji(
        row[0],
        KANGXI_RADICALS[row[1] - 1],  # Subtract 1 since list is 0-based.
        pickle.loads(row[2], fix_imports=False),
        pickle.loads(row[3], fix_imports=False),
        pickle.loads(row[4], fix_imports=False),
        row[5],
        row[6],
    )


# TODO(orphen) Revisit database schema or backing database choice to avoid serializing
# fields with types such as list. The current implementation prohibits directly querying
# things such as kanji readings.
def _build(kanjidic2_xml_pathname: str, database_pathname: Optional[str]):
    """
    Build an SQLite database containing all jouyou kanji. This function unconditionally
    deletes any existing database created previously by this function and creates a new
    database in the old one's place.

    :param kanjidic2_xml_pathname: A pathname to a kanjidic2 XML file. The database is
        built using content from this file.
    :type kanjidic2_xml_pathname: str
    :param database_pathname: The pathname to the database file to create on disk. This
        parameter is meant for use in tests. Ordinarily, pass `None` to have libjyk use
        an internal name.
    :type database_pathname: Optional[str]
    :return: The number of entries in the database.
    :rtype: int
    """
    if not database_pathname:
        create_persistent_jyk_paths()
        database_pathname = JYK_DEFAULT_DB
    conn = sqlite3.connect(database_pathname)
    cursor = conn.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {JOUYOU_TABLE_NAME}")
    cursor.execute(
        f"CREATE TABLE {JOUYOU_TABLE_NAME}({', '.join(JOUYOU_TABLE_ROW_NAMES)})"
    )

    for k in parse_kanjidic2(kanjidic2_xml_pathname):
        if k.kanji in JOUYOU_KANJI:
            cursor.execute(
                f"INSERT INTO {JOUYOU_TABLE_NAME} VALUES(?, ?, ?, ?, ?, ?, ?)",
                _kanji_to_row(k),
            )

    conn.commit()

    count = cursor.execute(f"SELECT COUNT(*) FROM {JOUYOU_TABLE_NAME}").fetchone()[0]
    return count


def build(kanjidic2_xml_pathname: str):
    """
    Build an SQLite database containing all jouyou kanji. This function unconditionally
    deletes any existing database created previously by this function and creates a new
    database in the old one's place.

    :param kanjidic2_xml_pathname: A pathname to a kanjidic2 XML file. The database is
        built using content from this file.
    :type kanjidic2_xml_pathname: str
    """
    num_db_entries = _build(kanjidic2_xml_pathname)
    assert num_db_entries == len(
        JOUYOU_KANJI
    ), "Unexpected number of kanji in database."
