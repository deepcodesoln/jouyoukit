from os.path import dirname, join

from libjyk.parser.kanjidic2 import parse_kanjidic2


def test_parse_kanjidic2():
    """
    This is a non-exhaustive test that reads a reduced version of the kanjidic2 XML file
    containing the header and a single kanji entry.
    """
    kanjidic2_subset_pathname = join(dirname(__file__), "assets/kanjidic2_subset.xml")
    for k in parse_kanjidic2(kanjidic2_subset_pathname):
        assert k.kanji == "亜", "Unexpected kanji literal."
        assert k.radical.radical == "二", "Unexpected radical."
        assert k.onyomi[0].reading == "ア", "Unexpected on'yomi."
        assert k.kunyomi[0].reading == "つ", "Unexpected kun'yomi."
        assert k.meanings == [
            "Asia",
            "rank next",
            "come after",
            "-ous",
        ], "Unexpected meanings."
        assert k.grade == 8, "Unexpected grade."
        assert k.frequency == 1509, "Unexpected frequency."
