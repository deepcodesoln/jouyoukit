from os.path import dirname, join

from libjyk.parser.kanjidic2 import parse_kanjidic2
from tests.utils import assert_ichi


def test_parse_kanjidic2():
    """
    This is a non-exhaustive test that reads a reduced version of the kanjidic2 XML file
    containing the header and a single kanji entry.
    """
    expected_kanji = {"一", "引", "悪", "愛", "圧", "胃", "亜"}

    kanjidic2_subset_pathname = join(dirname(__file__), "assets/kanjidic2_subset.xml")
    kanji_list = list(parse_kanjidic2(kanjidic2_subset_pathname))
    assert len(kanji_list) == 7, "Unexpected number of kanji in the kanjidic2 subset."

    for k in kanji_list:
        assert k.kanji in expected_kanji, "Unexpected kanji in the kanjidic2 subset."

        if k.kanji == "一":
            assert_ichi(k)
