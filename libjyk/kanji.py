"""This module contains a types representing Kanji and their metadata."""

from typing import NamedTuple, Optional

from libjyk.kangxi_radicals import Radical


class Reading(NamedTuple):
    """
    A single kanji reading and an optional indicator for whether the reading is in the
    joyou set.
    """

    reading: str
    is_jouyou: Optional[bool]

    def __str__(self):
        return reading

    def __hash__(self):
        # Allow hash collisions for two Readings with the same `reading` but different
        # `is_jouyou` values. Readings are identical if their `reading`s are the same.
        return hash(self.reading)

    def __eq__(self, other):
        # Disregard `is_jouyou` is equality check.
        # TODO(orphen) Revisit this decision since this behavior is perhaps more
        # surprising than `self.__hash__`.
        return self.reading == other.reading


class Kanji(NamedTuple):
    # The literal character for the kanji.
    kanji: str

    # The literal Kangxi character for the kanji's radical.
    radical: Radical

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

    def __str__(self):
        return (
            f"{self.kanji}: "
            f"radical: {self.radical}; "
            f"onyomi: {', '.join([reading.reading for reading in self.onyomi])}; "
            f"kunyomi: {', '.join([reading.reading for reading in self.kunyomi])}; "
            f"meanings: {', '.join(self.meanings)}; "
            f"grade: {self.grade}; "
            f"frequency: {self.frequency}"
        )