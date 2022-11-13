from libjyk import query


def test_libjyk_query_is_jouyou():
    assert query.is_jouyou("猫"), "猫 expected but not found in the jouyou kanji."
    assert not query.is_jouyou("釦"), "釦 not expected but found in the jouyou kanji."
    assert not query.is_jouyou("猫釦"), "猫釦 not expected but found in the jouyou kanji."
