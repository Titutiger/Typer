import json
from pathlib import Path
from wordfreq import zipf_frequency

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

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    # ---------------- CORE ----------------

    def get(self, word):
        """
        Priority:
        1. User-learned frequency
        2. Seeded wordfreq score
        3. Zero
        """
        if word in self.data:
            return self.data[word]

        # Lazy seed from wordfreq
        z = zipf_frequency(word, "en")
        if z > 0:
            score = int(z * 10)  # scale to int
            self.data[word] = score
            self.save()
            return score

        return 0

    def inc(self, word):
        self.data[word] = self.get(word) + 1
        self.save()


FREQ = FrequencyStore(FREQ_PATH)
