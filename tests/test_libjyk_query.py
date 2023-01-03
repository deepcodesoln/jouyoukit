import sqlite3
from os.path import dirname, join
from tempfile import NamedTemporaryFile
from unittest.mock import patch

from libjyk import query
from libjyk.jykdb import _build
from tests.utils import assert_ichi


TEMP_DB = NamedTemporaryFile(prefix="libjyk")


def get_db_connection():
    """
    This function provides connections to this test's temporary database. The function is
    meant to patch that of a similar name in libjyk.query.
    """
    conn = sqlite3.connect(TEMP_DB.name)
    query._assert_table_exists(conn)
    return conn


def setup_module():
    """Build the libjyk subset of the kanjidic2 database for tests in this module."""
    kanjidic2_subset_pathname = join(dirname(__file__), "assets/kanjidic2_subset.xml")
    num_entries = _build(kanjidic2_subset_pathname, TEMP_DB.name)


@patch("libjyk.query._get_db_connection", get_db_connection)
def test_libjyk_query_get_kanji():
    k = query.get_kanji("一")
    assert_ichi(k)
    k = query.get_kanji("犬")
    assert k is None, "Did not expect 犬 in the libjyk kanjidic2 subset."


@patch("libjyk.query._get_db_connection", get_db_connection)
def test_libjyk_query_get_kanji_for_grade():
    ks = query.get_kanji_for_grade(1, None)
    assert len(ks) == 1, "Unexpected number of kanji for grade 1 in test."
    assert_ichi(ks[0])


@patch("libjyk.query._get_db_connection", get_db_connection)
def test_libjyk_query_get_radicals_for_grade():
    rs = query.get_radicals_for_grade(1, None)
    assert len(rs) == 1, "Unexpected number of radicals for grade 1 in test database."
    assert rs[0].radical == "一", "Unexpected radical for grade 1 in test database."


@patch("libjyk.query._get_db_connection", get_db_connection)
def test_libjyk_query_get_radicals_unique_to_grade():
    rs = query.get_radicals_unique_to_grade(1, None)
    assert len(rs) == 1, "Unexpected number of unique radicals for grade 1 in test db."
    assert rs[0].radical == "一", "Unexpected unique radical for grade 1 in test db."


@patch("libjyk.query._get_db_connection", get_db_connection)
def test_libjyk_query_get_radicals_unique_to_grade():
    rs = query.get_radicals_introduced_in_grade(2, None)
    assert len(rs) == 1, "Unexpected number of radicals introduced in grade 2."
    assert rs[0].radical == "弓", "Unexpected radical introduced in grade 2."


def test_libjyk_query_is_jouyou():
    assert query.is_jouyou("猫"), "猫 expected but not found in the jouyou kanji."
    assert not query.is_jouyou("釦"), "釦 not expected but found in the jouyou kanji."
    assert not query.is_jouyou("猫釦"), "猫釦 not expected but found in the jouyou kanji."
