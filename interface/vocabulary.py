import json

class Vocabulary():
    def __init__(self, term: str, readings: list[str], meanings: list[str]):
        self.term = term
        self.readings = readings
        self.meanings = meanings

    def __repr__(self):
        return f"{self.term}; readings: {self.readings}; meanings: {self.meanings}"
