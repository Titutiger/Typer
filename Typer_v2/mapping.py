# mapping.py
from pathlib import Path

DROP_VOWELS = False
VOWELS = set("a") # aeiou

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
