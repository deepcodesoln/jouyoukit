import csv
import json
import xml.etree.ElementTree as ET

from jouyoukit.interface.kanji import Kanji
from jouyoukit.interface.radical import KANGXI_RADICALS
from jouyoukit.interface.vocabulary import Vocabulary


DB_FILE = "db.json"
NUM_JOUYOU = 2136
MAX_VOCAB_TERMS = 2
MAX_VOCAB_TERM_MEANINGS = 2

def parse_kanjidic(kanjidic2_xml_file: str) -> list[Kanji]:
    tree = ET.parse(kanjidic2_xml_file)
    root = tree.getroot()
    
    jouyou_kanji = []
    for character in root.findall("character"):
        misc = character.find("misc")
        if misc is None:
            continue
        for grade in misc.findall("grade"):
            if grade.text not in ["1", "2", "3", "4", "5", "6", "8"]:
                continue

            literal = character.find("literal").text

            radical = None
            for rad in character.findall("radical/rad_value"):
                if rad.get("rad_type") == "classical":
                    radical = KANGXI_RADICALS[int(rad.text) - 1]
                    break

            onyomi = []
            kunyomi = []
            for rmgroup in character.findall("reading_meaning/rmgroup"):
                for reading in rmgroup.findall("reading"):
                    if reading.get("r_type") == "ja_on":
                        if reading.text not in onyomi:
                            onyomi.append(reading.text)
                    elif reading.get("r_type") == "ja_kun":
                        kun_san = reading.text.split(".")[0].replace("-", "")
                        if kun_san not in kunyomi:
                            kunyomi.append(kun_san)

            meanings = []
            for meaning_group in character.findall("reading_meaning/rmgroup"):
                for meaning in meaning_group.findall("meaning"):
                    if "m_lang" not in meaning.attrib:
                        meanings.append(meaning.text)

            frequency = 9999
            freq_elem = misc.find("freq")
            if freq_elem is not None:
                frequency = int(freq_elem.text)
            
            jouyou_kanji.append(Kanji(literal, radical, onyomi, kunyomi, meanings, int(grade.text), frequency))
            break
    return jouyou_kanji

def parse_jmdict(kanji: list[Kanji], jmdict_xml_file) -> list[Kanji]:
    tree = ET.parse(jmdict_xml_file)
    root = tree.getroot()

    for entry in root.findall("entry"):
        for k_ele in entry.findall("k_ele"):
            ke_pri = k_ele.find("ke_pri")
            if ke_pri is None or ke_pri.text not in ["news1", "ichi1", "spec1", "gai1"]:
                break

            keb = k_ele.find("keb")
            if keb is None:
                break

            target_kanji = None
            for k in kanji:
                if k.char == keb.text: # Vocab is identical to kanji.
                    continue
                if k.char in keb.text and len(k.vocabulary) < MAX_VOCAB_TERMS:
                    target_kanji = k
                    break
            if target_kanji is None:
                break

            readings = [rele.find("reb").text for rele in entry.findall("r_ele")]
            meanings = [meaning.text for sense in entry.findall("sense") for meaning in sense.findall("gloss")]
            meanings = meanings[:MAX_VOCAB_TERM_MEANINGS]
            target_kanji.vocabulary.append(Vocabulary(keb.text, readings, meanings))
            break

    return kanji

def build_db(args):
    jk = parse_kanjidic(args.kanjidic2)
    assert len(jk) == NUM_JOUYOU
    jk = parse_jmdict(jk, args.jmdict)

    with open(DB_FILE, "w") as f:
        json.dump(jk, f, default=lambda o: o.to_json())

def to_csv_file(kanji: list[Kanji], csv_filename):
    with open(csv_filename, "w", newline='') as f:
        w = csv.writer(f)
        for k in kanji:
            r = f"{k.radical.char}"
            if k.radical.variants:
                r += f' ({", ".join(k.radical.variants)})'

            assert len(k.vocabulary) <= MAX_VOCAB_TERMS
            v1_term, v1_readings, v1_meanings = "", "", ""
            if len(k.vocabulary) > 0:
                v = k.vocabulary[0]
                v1_term, v1_readings, v1_meanings = v.term, v.readings, v.meanings
            v2_term, v2_readings, v2_meanings = "", "", ""
            if len(k.vocabulary) > 1:
                v = k.vocabulary[1]
                v2_term, v2_readings, v2_meanings = v.term, v.readings, v.meanings

            w.writerow([
                k.char,
                r,
                ", ".join(k.onyomi),
                ", ".join(k.kunyomi),
                ", ".join(k.meanings),
                k.grade,
                k.frequency,
                v1_term,
                ", ".join(v1_readings),
                ", ".join(v1_meanings),
                v2_term,
                ", ".join(v2_readings),
                ", ".join(v2_meanings)
            ])

def db_to_csv(_args):
    with open(DB_FILE, "r") as f:
        jk = json.load(f)
    kanji = [Kanji.from_json(kanji_json) for kanji_json in jk]

    def kanji_for_grade(kanji: list[Kanji], grade: int) -> list[Kanji]:
        return [k for k in kanji if k.grade == grade]

    # Split kanji by grades, sort by frequency.
    k1 = sorted(kanji_for_grade(kanji, 1), key=lambda k: k.frequency)
    k2 = sorted(kanji_for_grade(kanji, 2), key=lambda k: k.frequency)
    k3 = sorted(kanji_for_grade(kanji, 3), key=lambda k: k.frequency)
    k4 = sorted(kanji_for_grade(kanji, 4), key=lambda k: k.frequency)
    k5 = sorted(kanji_for_grade(kanji, 5), key=lambda k: k.frequency)
    k6 = sorted(kanji_for_grade(kanji, 6), key=lambda k: k.frequency)
    k8 = sorted(kanji_for_grade(kanji, 8), key=lambda k: k.frequency)

    # Write Anki CSV. Grade 8 is special. We split it into 10 levels.
    k1_csv = to_csv_file(k1, "1.csv")
    k2_csv = to_csv_file(k2, "2.csv")
    k3_csv = to_csv_file(k3, "3.csv")
    k4_csv = to_csv_file(k4, "4.csv")
    k5_csv = to_csv_file(k5, "5.csv")
    k6_csv = to_csv_file(k6, "6.csv")

    KANJI_PER_LEVEL = 111
    assert len(k8) % KANJI_PER_LEVEL == 0
    for i in range(10):
        start = KANJI_PER_LEVEL * i
        to_csv_file(k8[start:start + KANJI_PER_LEVEL], f"8.{i}.csv")


