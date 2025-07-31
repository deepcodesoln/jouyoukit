import json

from jouyoukit.interface.radical import Radical
from jouyoukit.interface.vocabulary import Vocabulary

class Kanji:
    def __init__(
        self,
        char: str,
        radical: Radical,
        onyomi: list[str],
        kunyomi: list[str],
        meanings: list[str],
        grade: int,
        frequency: int,
        vocabulary: list[Vocabulary] = None,
    ):
        self.char = char
        self.radical = radical
        self.onyomi = onyomi
        self.kunyomi = kunyomi
        self.meanings = meanings
        self.grade = grade
        self.frequency = frequency
        self.vocabulary = [] if vocabulary is None else vocabulary

    def __repr__(self):
        return f"{self.char}; radical: ({self.radical}); " +\
               f"on: {self.onyomi}; kun: {self.kunyomi}; meanings: {self.meanings}; " +\
               f"grade: {self.grade}; frequency: {self.frequency}; " +\
               f"vocabulary: {self.vocabulary}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @classmethod
    def from_json(cls, json_str: str):
        d = json.loads(json_str)

        rd = d["radical"]
        radical = Radical(rd["char"], rd["variants"], rd["meanings"], rd["num"])

        vd = d["vocabulary"]
        vocabulary = [Vocabulary(v["term"], v["readings"], v["meanings"]) for v in vd]

        return cls(
            d["char"],
            radical,
            d["onyomi"],
            d["kunyomi"],
            d["meanings"],
            int(d["grade"]),
            d["frequency"],
            vocabulary
        )
