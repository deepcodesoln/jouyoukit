import logging
import xml
import xml.etree.ElementTree as ET

from libjyk.kanji import Kanji, Reading
from libjyk.radicals import KANGXI_RADICALS
from libjyk.logging import LIBJYK_LOGGER_NAME


def _log_header(e: xml.etree.ElementTree.Element):
    """
    Log the contents of the kanjidic2 header as debug information.

    :param e: The header element from a kanjidic2 XML tree.
    :type e: xml.etree.ElementTree.Element
    """
    assert e.tag == "header", f"Expected header element, received {e.tag}."

    file_ver = e[0]
    database_ver = e[1]
    created = e[2]

    logger = logging.getLogger(LIBJYK_LOGGER_NAME)
    logging.debug(
        "kanjidic2 metadata: file ver.: {}, db ver.: {}, created: {}".format(
            file_ver.text, database_ver.text, created.text
        )
    )


def print_element(e: xml.etree.ElementTree.Element):
    print(e.tag, e.attrib, e.text)


def _parse_kanji(e: xml.etree.ElementTree.Element) -> Kanji:
    """
    Parse information from a single character element from a kanjidic2 XML tree.

    :param e: A character element from a kanjidic2 XML tree.
    :type e: xml.etree.ElementTree.Element
    :return: The parsed kanji infromation as a :class:`Kanji` instance.
    :rtype: Kanji
    """
    # This parsing follows the kanjidic2 DTD:
    # https://www.edrdg.org/kanjidic/kanjidic2_dtdh.html

    assert e.tag == "character", f"Expected character element, received {e.tag}."

    # Parse the kanji literal.
    kanji = e.find("literal").text

    # Parse the kanji radical.
    radical = None
    for rad in e.find("radical"):
        if rad.attrib["rad_type"] == "classical":  # Kangxi as opposed to Nelson.
            radical = KANGXI_RADICALS[int(rad.text) - 1]
            break

    # Parse the grade and frequency.
    misc = e.find("misc")
    grade = None
    if (grade_element := misc.find("grade")) is not None:
        grade = int(grade_element.text)
    frequency = None
    if (frequency_element := misc.find("freq")) is not None:
        frequency = int(frequency_element.text)

    # codepoint = e[1]
    # dic_number = e[4]
    # query_code = e[5]

    # Parse the readings and meanings.
    reading_meaning = e.find("reading_meaning")
    onyomi: list[Reading] = []
    kunyomi: list[Reading] = []
    meanings: list[str] = []

    # Some entries, such as "𠂉," have no reading or meaning.
    if not reading_meaning:
        return Kanji(kanji, radical, onyomi, kunyomi, meanings, grade, frequency)

    for rmgroup in reading_meaning.iter("rmgroup"):
        for reading in rmgroup.iter("reading"):
            is_jouyou = None
            if reading.attrib["r_type"] == "ja_on":
                if "r_status" in reading.attrib:
                    is_jouyou = reading.attrib["r_status"] == "jy"
                onyomi.append(Reading(reading.text, is_jouyou))
            elif reading.attrib["r_type"] == "ja_kun":
                if "r_status" in reading.attrib:
                    is_jouyou = reading.attrib["r_status"] == "jy"
                if "." in reading.text:
                    read = reading.text.split(".")[0]
                else:
                    read = reading.text
                kunyomi.append(Reading(read, is_jouyou))
        for meaning in rmgroup.iter("meaning"):
            if "m_lang" not in meaning.attrib or meaning.attrib["m_lang"] == "en":
                meanings.append(meaning.text)

        # Filter out duplicate kunyomi readings resulting from how we handled `.`.
        kunyomi = list(dict.fromkeys(kunyomi))

    return Kanji(kanji, radical, onyomi, kunyomi, meanings, grade, frequency)


def parse_kanjidic2(pathname: str):
    """
    Parse individual kanji entries out of a kanjidic2 XML file. The parsing is not
    secure against malicious file content. It is the caller's responsibility to
    make sure they trust the content that will be parsed.

    :param pathname: The pathname of the kanjidic2 XML file.
    :type pathname: str
    :return: A generator that yields :class:`Kanji` instances for each kanji in the
        kanjidic2 file.
    :rtype: generator
    """
    tree = ET.parse(pathname)
    root = tree.getroot()

    for child in root:
        if child.tag == "character":
            yield _parse_kanji(child)
        elif child.tag == "header":
            # The header should only appear once in the file, so we'll miss this branch
            # 99% of the time. Therefore, we check for "header" after "character."
            _log_header(child)
