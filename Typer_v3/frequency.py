import json
from pathlib import Path

FREQ_PATH = Path(__file__).parent / "data" / "words_dictionary.json"


class FrequencyStore:
    def __init__(self, path):
        self.path = path
        self.data = self._load()

    def _load(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get(self, word):
        return self.data.get(word, 0)

    def inc(self, word):
        self.data[word] = self.get(word) + 1
        self.save()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)


FREQ = FrequencyStore(FREQ_PATH)
