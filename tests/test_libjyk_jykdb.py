import sqlite3
from tempfile import NamedTemporaryFile
from os.path import dirname, join

from libjyk.jykdb import JOUYOU_TABLE_NAME, _build, row_to_kanji
from tests.utils import assert_ichi


def test_libjyk_jykdb_build():
    """
    Build a temporary database and then execute some queries on it to confirm its
    contents.
    """
    temp_db = NamedTemporaryFile(prefix="libjyk")
    kanjidic2_subset_pathname = join(dirname(__file__), "assets/kanjidic2_subset.xml")
    num_entries = _build(kanjidic2_subset_pathname, temp_db.name)
    assert num_entries == 7

    conn = sqlite3.connect(temp_db.name)
    cursor = conn.cursor()

    res = cursor.execute(f"SELECT * FROM {JOUYOU_TABLE_NAME} WHERE grade=1").fetchone()
    k = row_to_kanji(res)
    assert_ichi(k)
