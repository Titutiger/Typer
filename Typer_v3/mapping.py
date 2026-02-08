# mapping.py
from wordfreq import top_n_list
from pathlib import Path
from Typer_v3.frequency import FREQ

DROP_VOWELS = False
VOWELS = set("a") # aeiou
MAX_WORDFREQ_CANDIDATES = 5000

def normalize(text: str) -> str:
    text = text.lower()
    text = "".join(c for c in text if c not in VOWELS)  # optional
    return "".join(sorted(set(text)))

def add_word(word: str):
    sig = normalize(word)
    if sig not in WORD_MAP:
        WORD_MAP[sig] = []
    if word not in WORD_MAP[sig]:
        WORD_MAP[sig].append(word)
    WORD_MAP[sig].sort(key=lambda w: FREQ.get(w), reverse=True)

def try_load_from_json(sig: str) -> list[str]:
    """Load words with this signature from words_dictionary.json if not in WORD_MAP"""
    if sig in WORD_MAP:
        return WORD_MAP[sig]

    loaded_words = []
    for word in FREQ.data.keys():
        if normalize(word) == sig:
            loaded_words.append(word)

    if loaded_words:
        loaded_words.sort(key=lambda w: FREQ.get(w), reverse=True)
        WORD_MAP[sig] = loaded_words

    return loaded_words

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


def wordfreq_candidates(sig: str, exclude: set[str]) -> list[str]:
    results = []

    for word in top_n_list('en', MAX_WORDFREQ_CANDIDATES):
        if word in exclude:
            continue
        if normalize(word) == sig:
            # seed freq lazily
            FREQ.get(word)
            results.append(word)

    results.sort(key=lambda w: FREQ.get(w), reverse=True)
    return results

# Load once (important for performance)
WORDS = load_wordlist()
WORD_MAP = build_mapping(WORDS)
