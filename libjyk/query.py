"""
This module provides functions to query the collection of jouyou kanji for
various information.
"""

from libjyk.jouyou_kanji import JOUYOU_KANJI


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
