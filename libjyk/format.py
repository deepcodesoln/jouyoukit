import csv
from io import StringIO

from libjyk.kanji import Kanji


"""A list of supported tool output formats."""
SUPPORTED_FORMATS = ["csv"]


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
