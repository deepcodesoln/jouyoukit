"""
This module contains facilities for interacting with an existing jouyou toolkit kanji
database.
"""

import os
import pickle
import sqlite3
from typing import Optional

from libjyk.jykdb.build import (
    JOUYOU_TABLE_NAME,
    JOUYOU_TABLE_ROW_SCHEMA,
    JYK_DEFAULT_DB,
)
from libjyk.kanji import Kanji
from libjyk.radicals import KANGXI_RADICALS


class TableDoesNotExist(Exception):
    pass


"""A list of school grades in which kanji are taught. 8 indicates secondary school."""
KANJI_GRADES = [1, 2, 3, 4, 5, 6, 8]


"""A list of supported database columns to sort by."""
SUPPORTED_SORT = ["frequency"]


def _assert_table_exists(conn):
    """
    Check that the jouyou toolkit database exists.
    :param conn: An active connection to the JYK_DEFAULT_DB.
    :type conn: sqlite3.Connection
    :raises TableDoesNotExist: Raised if the required jouyou database does not exist.
    """
    res = conn.cursor().execute("SELECT name FROM sqlite_master").fetchall()
    for name in res:
        if JOUYOU_TABLE_NAME in name:
            return
    raise TableDoesNotExist()


def _row_to_kanji(row: JOUYOU_TABLE_ROW_SCHEMA) -> Kanji:
    """
    :param row: A row from JOUYOU_TABLE_NAME.
    :type row: JOUYOU_TABLE_KANJI_SCHEMA.
    :return: The database row represented as a Kanji instance.
    :rtype: Kanji
    """
    return Kanji(
        row[0],
        KANGXI_RADICALS[row[1] - 1],  # -1 since list is 0-based.
        pickle.loads(row[2], fix_imports=False),
        pickle.loads(row[3], fix_imports=False),
        pickle.loads(row[4], fix_imports=False),
        row[5],
        row[6],
    )


def get_kanji(literal: str) -> Optional[Kanji]:
    """
    :param literal: The kanji literal to search for.
    :type literal: str
    :return: Information on the kanji if its in the database, otherwise `None`.
    :rtype: Optional[Kanji]
    :raises TableDoesNotExist: Raised if the required jouyou database does not exist.
    """
    conn = sqlite3.connect(os.path.expanduser(JYK_DEFAULT_DB))
    _assert_table_exists(conn)

    cursor = conn.cursor()
    res = cursor.execute(f"SELECT * from {JOUYOU_TABLE_NAME} WHERE kanji='{literal}'")
    entry = res.fetchone()
    return _row_to_kanji(entry) if entry else None


def get_kanji_by_grade(grade: int, sort_by: Optional[str]) -> list[Kanji]:
    """
    :param grade: The grade to filter kanji by. Must be one of KANJI_GRADES.
    :type grade: int
    :param sort_by: The column name to sort query results by. `None` indicates no sort.
    :type sort_by: Optional[str]
    :return: A list of instances of Kanji for a specific grade.
    :rtype: list[Kanji]
    :raises TableDoesNotExist: Raised if the required jouyou database does not exist.
    """
    assert grade in KANJI_GRADES, f"Unsupported grade: {grade}."

    conn = sqlite3.connect(os.path.expanduser(JYK_DEFAULT_DB))
    _assert_table_exists(conn)

    cursor = conn.cursor()
    sort = f"ORDER BY IFNULL({sort_by}, 9999)" if sort_by else ""
    res = cursor.execute(
        f"SELECT * from {JOUYOU_TABLE_NAME} WHERE grade={grade} {sort}"
    )
    return [_row_to_kanji(r) for r in res.fetchall()]
