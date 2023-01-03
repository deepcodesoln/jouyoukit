from libjyk.kanji import JOUYOU_KANJI


def test_jouyou_kanji_length():
    """
    This is a sanity test to make sure the embedded jouyou kanji list is at least as long
    as we expecte it to be. This does not guarantee the contents.
    """
    assert len(JOUYOU_KANJI) == 2136, "Unexpected number of jouyou kanji."
