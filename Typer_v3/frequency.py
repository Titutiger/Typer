# frequency.py
import json
from pathlib import Path
from wordfreq import top_n_list

from Typer_v3.mapping import sig_counter, is_subset


FREQ_PATH = Path(__file__).parent / "data" / "words_dictionary.json"


def get_wordfreq_matches(typed_sig, exclude, limit=20):
    results = []

    for word in top_n_list("en", 50000):
        if word in exclude:
            continue
        if is_subset(typed_sig, sig_counter(word)):
            results.append(word)
        if len(results) >= limit:
            break

    return results


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
