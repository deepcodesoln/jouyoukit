from libjyk.kanji import Kanji
from libjyk.radicals import KANGXI_RADICALS


def assert_ichi(kanji: Kanji):
    """
    Assert that `kanji` is ichi (一) with ichi's correct properties.

    :param kanji: The Kanji instance to compare against ichi's properties.
    :type kanji: Kanji
    """
    assert kanji.kanji == "一"
    assert kanji.radical == KANGXI_RADICALS[0]
    onyomi = [r.reading for r in kanji.onyomi]
    assert onyomi == ["イチ", "イツ"], "Unexpected on'yomi."
    kunyomi = [r.reading for r in kanji.kunyomi]
    assert kunyomi == ["ひと-", "ひと"], "Unexpected kun'yomi."
    assert kanji.meanings == ["one", "one radical (no.1)"], "Unexpected meanings."
    assert kanji.grade == 1, "Unexpected grade."
    assert kanji.frequency == 2, "Unexpected frequency."
