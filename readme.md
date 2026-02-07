from Typer_v2.input import STENO_TRIGGER

# Typer_v2 — Adaptive Steno Typing Engine

Typer_v2 is a lightweight, real-time **stenography-style typing engine** for Python that expands short, unordered letter chords into full words — and **learns from your usage over time**.

Think:  
`clo → cool`  
`aet → eat / tea / ate` (cycle with →)  
`twtr → twitter` (vowel-insensitive)

No massive hotkey maps. No hardcoded shortcuts. Just logic + learning.

---

## ✨ Features

- 🔤 **Order-insensitive matching**
  - Letters can be typed in any order
  - `clo`, `loc`, `ocl` → `cool`

- 🔄 **Cycling candidates**
  - Press **Right Arrow** to cycle through matching words

- 🧠 **Frequency learning**
  - The engine remembers which word *you* pick
  - Most-used words automatically rise to the top

- ⌨️ **Non-intrusive**
  - Only activates after a trigger key (`;`)
  - Ignores non-alphabetic keys unless relevant

- ⚡ **Low latency**
  - Expands after a short configurable delay
  - No blocking, no laggy UI

---

## 🧩 How It Works

1. Press the **steno trigger** (`;`)
2. Type up to **4 letters** (unordered)
3. Engine normalizes input and finds matches
4. Best match is auto-expanded
5. Press **→** to cycle alternatives
6. Press **Space / Enter** to commit (and learn!)

Example:

```commandline
;clo -> cool -> coal
;aet -> eat -> tea -> ate
```

___

Project Structure:
```commandline
Typer_v2/
│── __init__.py
│── input.py
│── mapping.py
│── cycle.py
│── frequency.py
│
└── data/
    │── words.txt
    │── words_alpha.txt
    └── words_dictionary.json
```


---

## 📚 Word List

The engine builds its vocabulary from:
```commandline
data/words_dictionary.json
```
Credit: https://github.com/dwyl/english-words?tab=readme-ov-file

___

## ⚙️ Configuration

`input.py`

```python
STENO_TRIGGER: str = ';'
EXPAND_DELAY: float = 0.18
```

___

## Installaton

> [!] Note that this may require root privilege!

```commandline
requirements.txt
```

