import csv
from io import StringIO

from libjyk.kanji import Kanji
from libjyk.kangxi_radicals import Radical


"""A list of supported tool output formats."""
SUPPORTED_FORMATS = ["csv"]


def radical_list_to_csv(radicals: list[Radical]) -> str:
    """
    Convert a list of Radical instances into CSV text. The text has the row schema:
        radical, variants, meanings

    :param radicals: A list of Radical instances to convert to CSV.
    :type radicals: list[Radical]
    :return: The list of Radical instances formatted as CSV.
    :rtype: str
    """
    buffer = StringIO()
    writer = csv.writer(buffer)

    for r in radicals:
        writer.writerow(
            [
                r.radical,
                ", ".join([v for v in r.variants]),
                ", ".join([m for m in r.meanings]),
            ]
        )

    s = buffer.getvalue()
    buffer.close()
    return s


def kanji_list_to_csv(kanji: list[Kanji]) -> str:
    """
    Convert a list of Kanji instances into CSV text. The text has the row schema:
        kanji, radical, on'yomi, kun'yomi, meanings, grade, frequency

    :param kanji: A list of Kanji instances to convert to CSV.
    :type kanji: list[Kanji]
    :return: The list of Kanji instances formatted as CSV.
    :rtype: str
    """
    buffer = StringIO()
    writer = csv.writer(buffer)

    for k in kanji:
        writer.writerow(
            [
                k.kanji,
                k.radical,
                ", ".join([o.reading for o in k.onyomi]),
                ", ".join([k.reading for k in k.kunyomi]),
                ", ".join([m for m in k.meanings]),
                k.grade,
                k.frequency,
            ]
        )

    s = buffer.getvalue()
    buffer.close()

    return s
