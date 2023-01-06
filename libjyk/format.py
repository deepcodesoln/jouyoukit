import csv
from enum import Enum
from io import StringIO
from typing import Optional

from libjyk.kanji import Kanji
from libjyk.radicals import Radical
from libjyk.query import KANJI_GRADES


class SlugComponent(Enum):
    """A slug component differentiates content of different type for the same grade."""

    RADICAL = 0
    KANJI = 1


"""A list of supported tool output formats."""
SUPPORTED_FORMATS = ["csv"]


def radical_csv_header() -> list[str]:
    """
    :return: A list of column headers for radicals represented as CSV.
    :rtype: list[str]
    """
    return ["radical", "variants", "meanings", "number", "slug"]


def radical_list_to_csv(radicals: list[Radical], grade: Optional[int]) -> str:
    """
    Convert a list of Radical instances into CSV text. The row schema is that provided by
    `radical_csv_header`.

    :param radicals: A list of Radical instances to convert to CSV.
    :type radicals: list[Radical]
    :param grade: A singular grade to use in creating the slug. If `None`, the slug
        suffix will be the radical number.
    :type grade: Optional[int]
    :return: The list of Radical instances formatted as CSV.
    :rtype: str
    """
    count_in_grade = 0

    buffer = StringIO()
    writer = csv.writer(buffer)

    for r in radicals:
        if grade:
            slug = f"{grade}_{SlugComponent.RADICAL.value}_{count_in_grade}"
            count_in_grade += 1
        else:
            slug = f"{SlugComponent.RADICAL.value}_{r.number}"

        writer.writerow(
            [
                r.radical,
                ", ".join([v for v in r.variants]),
                ", ".join([m for m in r.meanings]),
                r.number,
                slug,
            ]
        )

    s = buffer.getvalue()
    buffer.close()
    return s


def kanji_csv_header() -> list[str]:
    """
    :return: A list of column headers for Kanji represented as CSV.
    :rtype: list[str]
    """
    return [
        "kanji",
        "radical",
        "onyomi",
        "kunyomi",
        "meanings",
        "grade",
        "frequency",
        "slug",
    ]


def kanji_list_to_csv(kanji: list[Kanji], grade: Optional[int]) -> str:
    """
    Convert a list of Kanji instances into CSV text. The row schema is that provided by
    `kanji_csv_header`.

    :param kanji: A list of Kanji instances to convert to CSV.
    :type kanji: list[Kanji]
    :param grade: A singular grade to use in creating the slug. If `None`, the slug
        suffix will be the kanji.
    :type grade: Optional[int]

    :return: The list of Kanji instances formatted as CSV.
    :rtype: str
    """
    kanji_in_grade = 0

    buffer = StringIO()
    writer = csv.writer(buffer)

    for k in kanji:
        if grade:
            slug = f"{k.grade}_{SlugComponent.KANJI.value}_{kanji_in_grade}"
            kanji_in_grade += 1
        else:
            slug = f"{k.grade}_{SlugComponent.KANJI.value}_{k.kanji}"

        writer.writerow(
            [
                k.kanji,
                k.radical,
                ", ".join([o.reading for o in k.onyomi]),
                ", ".join([k.reading for k in k.kunyomi]),
                ", ".join([m for m in k.meanings]),
                k.grade,
                k.frequency,
                slug,
            ]
        )

    s = buffer.getvalue()
    buffer.close()

    return s
