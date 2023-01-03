"""
This module provides functions to query the collection of jouyou kanji for
various information.
"""

import pickle
import sqlite3
from typing import Optional

from libjyk.jykdb import (
    JOUYOU_TABLE_NAME,
    JOUYOU_TABLE_ROW_SCHEMA,
    JYK_DEFAULT_DB,
    row_to_kanji,
)
from libjyk.kanji import JOUYOU_KANJI, Kanji
from libjyk.radicals import KANGXI_RADICALS, Radical


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


def _get_db_connection():
    """
    Get a connection to the backing libjyk database. This function exists so that tests
    can patch it to get connections on databases other than that specified by
    JYK_DEFAULT_DB.
    :return: A connection to a backing database on disk.
    :rtype: sqlite3.Connection
    :raises TableDoesNotExist: Raised if the required jouyou database does not exist.
    """
    conn = sqlite3.connect(JYK_DEFAULT_DB)
    _assert_table_exists(conn)
    return conn


def get_kanji(literal: str) -> Optional[Kanji]:
    """
    :param literal: The kanji literal to search for.
    :type literal: str
    :return: Information on the kanji if its in the database, otherwise `None`.
    :rtype: Optional[Kanji]
    :raises TableDoesNotExist: Raised if the required jouyou database does not exist.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    res = cursor.execute(f"SELECT * from {JOUYOU_TABLE_NAME} WHERE kanji='{literal}'")
    entry = res.fetchone()
    return row_to_kanji(entry) if entry else None


def get_kanji_for_grade(grade: int, sort_by: Optional[str]) -> list[Kanji]:
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

    conn = _get_db_connection()
    cursor = conn.cursor()
    sort = f"ORDER BY IFNULL({sort_by}, 9999)" if sort_by else ""
    res = cursor.execute(
        f"SELECT * from {JOUYOU_TABLE_NAME} WHERE grade={grade} {sort}"
    )
    return [row_to_kanji(r) for r in res.fetchall()]


def get_radicals_for_grade(grade: int, sort_by: Optional[str]) -> list[Radical]:
    """
    :param grade: The grade to filter radicals by. Must be one of KANJI_GRADES.
    :type grade: int
    :param sort_by: The column name to sort query results by. `None` indicates no sort.
    :type sort_by: Optional[str]
    :return: A list of instances of Radical for a specific grade.
    :rtype: list[Radical]
    :raises TableDoesNotExist: Raised if the required jouyou database does not exist.
    """
    assert grade in KANJI_GRADES, f"Unsupported grade: {grade}."

    conn = _get_db_connection()
    cursor = conn.cursor()
    sort = f"ORDER BY IFULL({sort_by}, 9999)" if sort_by else ""
    res = cursor.execute(
        f"SELECT kangxi_radical from {JOUYOU_TABLE_NAME} WHERE grade={grade} {sort}"
    )
    return [KANGXI_RADICALS[r_code[0] - 1] for r_code in res.fetchall()]


def get_radicals_unique_to_grade(grade: int, sort_by: Optional[str]) -> list[Radical]:
    """
    :param grade: The grade to get unique radicals for. Must be one of KANJI_GRADES.
    :type grade: int
    :param sort_by: The column name to sort query results by. `None` indicates no sort.
    :type sort_by: Optional[str]
    :return: A list of instances of Radical unique to a specific grade.
    :rtype: list[Radical]
    :raises TableDoesNotExist: Raised if the required jouyou database does not exist.
    """
    assert grade in KANJI_GRADES, f"Unsupported grade: {grade}."

    conn = _get_db_connection()
    cursor = conn.cursor()
    sort = f"ORDER BY IFULL({sort_by}, 9999)" if sort_by else ""

    grade_radicals = cursor.execute(
        f"SELECT kangxi_radical from {JOUYOU_TABLE_NAME} WHERE grade={grade} {sort}"
    ).fetchall()
    other_radicals = cursor.execute(
        f"SELECT kangxi_radical from {JOUYOU_TABLE_NAME} WHERE grade!={grade} {sort}"
    ).fetchall()

    unique_radicals = set(grade_radicals) - set(other_radicals)
    return [KANGXI_RADICALS[r_code[0] - 1] for r_code in unique_radicals]


def get_radicals_introduced_in_grade(
    grade: int, sort_by: Optional[str]
) -> list[Radical]:
    """
    :param grade: The grade to get radicals new to all grades before for. Must be one of
                  KANJI_GRADES.
    :type grade: int
    :param sort_by: The column name to sort query results by. `None` indicates no sort.
    :type sort_by: Optional[str]
    :return: A list of instances of Radical new to all grades before `grade`.
    :rtype: list[Radical]
    :raises TableDoesNotExist: Raised if the required jouyou database does not exist.
    """
    assert grade in KANJI_GRADES, f"Unsupported grade: {grade}."

    conn = _get_db_connection()
    cursor = conn.cursor()
    sort = f"ORDER BY IFULL({sort_by}, 9999)" if sort_by else ""

    new_radicals = cursor.execute(
        f"SELECT kangxi_radical from {JOUYOU_TABLE_NAME} WHERE grade={grade} {sort}"
    ).fetchall()
    new_radicals = set(new_radicals)

    for g in KANJI_GRADES:
        if g == grade:
            break
        grade_radicals = cursor.execute(
            f"SELECT kangxi_radical from {JOUYOU_TABLE_NAME} WHERE grade={g} {sort}"
        ).fetchall()
        new_radicals -= set(grade_radicals)

    return [KANGXI_RADICALS[r_code[0] - 1] for r_code in new_radicals]


def is_jouyou(character: str) -> bool:
    """
    Check whether a character is in the set of jouyou kanji.

    :param character: The character to test for inclusion in the set of jouyou
        kanji.
    :type character: str
    :return: `True` if the character is in the set of jouyou kanji. `False`
        otherwise.
    :rtype: bool
    """
    return character in JOUYOU_KANJI
