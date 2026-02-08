# mapping.py
from pathlib import Path
from collections import Counter
import json

from Typer_v3.frequency import FREQ

DATA_PATH = Path(__file__).parent / "data" / "words_dictionary.json"
DROP_VOWELS = True
VOWELS = set("a") # aeiou
WORD_SIGS = {}

# LOADING BASE WORDS:
with open(DATA_PATH, "r") as f:
    ALL_WORDS = set(json.load(f).keys())

def normalize(text: str) -> str:
    text = text.lower()
    text = "".join(c for c in text if c not in VOWELS)  # optional
    return "".join(sorted(set(text)))


def load_wordlist():
    # project_root/data/words.txt
    base_dir = Path(__file__).resolve().parent
    wordlist_path = base_dir / "data" / "words_alpha.txt"

    if not wordlist_path.exists():
        raise FileNotFoundError(f"Wordlist not found at {wordlist_path}")

    with open(wordlist_path, "r", encoding="utf-8") as f:
        words = [
            line.strip().lower()
            for line in f
            if line.strip().isalpha()
        ]

    return words

def add_word(word: str):
    if word in ALL_WORDS:
        return

    ALL_WORDS.add(word)
    WORD_SIGS[word] = sig_counter(word)


def find_matches(typed_buffer: str, limit=10) -> list[str]:
    typed_sig = sig_counter(typed_buffer)

    matches = []
    for word, wsig in WORD_SIGS.items():
        if is_subset(typed_sig, wsig):
            matches.append(word)

    # Rank by learned frequency
    matches.sort(key=lambda w: FREQ.get(w), reverse=True)
    return matches[:limit]


def sig_counter(text: str) -> Counter:
    text = text.lower()
    if DROP_VOWELS:
        text = "".join(c for c in text if c not in VOWELS)
    return Counter(text)


# Build signature cache
for word in ALL_WORDS:
    WORD_SIGS[word] = sig_counter(word)

def is_subset(typed: Counter, word: Counter) -> bool:
    for c, n in typed.items():
        if word[c] < n:
            return False
    return True

def build_mapping(words):
    """
    signature -> [word1, word2, ...]
    """
    mapping = {}

    for word in words:
        sig = normalize(word)
        if len(sig) == 0:
            continue

        mapping.setdefault(sig, []).append(word)

    return mapping


# Load once (important for performance)
WORDS = load_wordlist()
WORD_MAP = build_mapping(WORDS)
