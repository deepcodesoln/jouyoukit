from libjyk.kangxi_radicals import KANGXI_RADICALS


def test_kangxi_radicals():
    """
    Look up some radicals to make sure that their index matches their Kangxi radical
    number. Remember that `KANGXI_RADICALS` is 0-based whereas radical numbers are
    1-based. This test is a non-comprehensive sanity check to make sure the Kangix
    radical list was copied correctly.
    """
    assert KANGXI_RADICALS[0].radical == "一", "Unexpected index for 一."
    assert KANGXI_RADICALS[213].radical == "龠", "Unexpected index for 龠."

    assert KANGXI_RADICALS[4].radical == "乙", "Unexpected index for 乙."
    assert KANGXI_RADICALS[20].radical == "匕", "Unexpected index for 匕."
    assert KANGXI_RADICALS[69].radical == "方", "Unexpected index for 方."

    assert KANGXI_RADICALS[139].radical == "艸", "Unexpected index for 艸."
    assert KANGXI_RADICALS[168].radical == "門", "Unexpected index for 門."
    assert KANGXI_RADICALS[204].radical == "黽", "Unexpected index for 黽."
