from libjyk.kangxi_radicals import KANGXI_RADICALS


def test_kangxi_radicals():
    """
    Look up some radicals to make sure that their index matches their Kangxi radical
    number. Remember that `KANGXI_RADICALS` is 0-based whereas radical numbers are
    1-based. This test is a non-comprehensive sanity check to make sure the Kangix
    radical list was copied correctly.
    """
    assert KANGXI_RADICALS.index("一") == 0, "Unexpected index for 一."
    assert KANGXI_RADICALS.index("龠") == 213, "Unexpected index for 龠."

    assert KANGXI_RADICALS.index("乙") == 4, "Unexpected index for 乙."
    assert KANGXI_RADICALS.index("匕") == 20, "Unexpected index for 匕."
    assert KANGXI_RADICALS.index("方") == 69, "Unexpected index for 方."

    assert KANGXI_RADICALS.index("艸") == 139, "Unexpected index for 艸."
    assert KANGXI_RADICALS.index("門") == 168, "Unexpected index for 門."
    assert KANGXI_RADICALS.index("黽") == 204, "Unexpected index for 黽."
