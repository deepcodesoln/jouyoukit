"""This module contains a types representing Kanji and their metadata."""

from typing import Optional

from typing import NamedTuple


class Reading(NamedTuple):
    """
    A single kanji reading and an optional indicator for whether the reading is in the
    joyou set.
    """

    reading: str
    is_jouyou: Optional[bool]


class Kanji(NamedTuple):
    # The literal character for the kanji.
    kanji: str

    # The literal Kangxi character for the kanji's radical.
    radical: str

    # A list of on'yomi readings.
    onyomi: list[Reading]

    # A list of kun'yomi readings.
    kunyomi: list[Reading]

    # A list of meanings.
    meanings: list[str]

    # The Japanese school grade in which the character is taught.
    # 1-6 indicate grades 1-6, 8 indicates the jouyou kanji not taught in grades 1-6,
    # `None` indicates the kanji does not belong to either group.
    grade: Optional[int]

    # The frequency among the 2,500 most common kanji found in newspapers. `None`
    # indicates that the kanji is outside of this group. 1 indicates the most frequent.
    frequency: Optional[int]
