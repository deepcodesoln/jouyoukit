import os
import pickle
import sqlite3

from libjyk.jykdb.database import (
    JOUYOU_TABLE_NAME,
    JOUYOU_TABLE_ROW_NAMES,
    JOUYOU_TABLE_ROW_SCHEMA,
)
from libjyk.jouyou_kanji import JOUYOU_KANJI
from libjyk.kanji import Kanji
from libjyk.parser.kanjidic2 import parse_kanjidic2
from libjyk.pathing import JYK_USER_DIR, create_persistent_jyk_paths


JYK_DEFAULT_DB = os.path.join(JYK_USER_DIR, "jyk.db")


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
        kanji.radical,
        pickle.dumps(kanji.onyomi, fix_imports=False),
        pickle.dumps(kanji.kunyomi, fix_imports=False),
        pickle.dumps(kanji.meanings, fix_imports=False),
        kanji.grade,
        kanji.frequency,
    )


# TODO(orphen) Revisit database schema or backing database choice to avoid serializing
# fields with types such as list. The current implementation prohibits directly querying
# things such as kanji readings.
def build(kanjidic2_xml_pathname: str):
    """
    Build an SQLite database containing all jouyou kanji. This function unconditionally
    deletes any existing database created previously by this function and creates a new
    database in the old one's place.

    :param kanjidic2_xml_pathname: A pathname to a kanjidic2 XML file. The database is
        built using content from this file.
    :type kanjidic2_xml_pathname: str
    """
    create_persistent_jyk_paths()
    jyk_db_path = os.path.expanduser(JYK_DEFAULT_DB)
    conn = sqlite3.connect(jyk_db_path)
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
    assert count == len(JOUYOU_KANJI), "Unexpected number of entries in new database."
