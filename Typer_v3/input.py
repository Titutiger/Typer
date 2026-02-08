# input.py
import keyboard
import threading

from Typer_v3.mapping import WORD_MAP, normalize, is_subset, sig_counter, find_matches
from Typer_v3.cycle import CycleState
from Typer_v3.frequency import FREQ, get_wordfreq_matches

# ================= CONFIG =================

STENO_TRIGGER = ";"
EXPAND_DELAY = 0.18

CONTROL_KEYS = {
    "space",
    "enter",
    "backspace",
    "right",
    "right arrow",
}

# ================= STATE =================

steno_active = False
typed_buffer = ""
expanded_word = ""

# number of characters to delete (from ';' to cursor)
steno_span_length = 0

suppress = False
expand_timer = None

cycle = CycleState()

# ================= HELPERS =================

def cancel_timer():
    global expand_timer
    if expand_timer:
        expand_timer.cancel()
        expand_timer = None


def delete_span():
    """Delete everything typed since ';'"""
    global suppress
    suppress = True
    for _ in range(steno_span_length):
        keyboard.send("backspace")
    suppress = False


def replace_word(new_word):
    """Replace entire steno span with new_word"""
    global expanded_word, steno_span_length

    delete_span()
    keyboard.write(new_word)

    expanded_word = new_word
    steno_span_length = len(new_word)


def rank_by_frequency(words):
    """Sort words by learned frequency (desc)"""
    return sorted(
        words,
        key=lambda w: FREQ.get(w),
        reverse=True
    )


def try_expand():
    global expanded_word

    if not steno_active:
        return

    if not typed_buffer or len(typed_buffer) > 6:
        return

    matches = find_matches(typed_buffer, limit=20)

    if not matches:
        return

    ranked = rank_by_frequency(matches)
    expanded_word = ""
    replace_word(ranked[0])



def schedule_expand():
    global expand_timer
    cancel_timer()
    expand_timer = threading.Timer(EXPAND_DELAY, try_expand)
    expand_timer.start()


def reset_state(commit=False):
    """Reset steno state and optionally learn frequency"""
    global steno_active, typed_buffer, expanded_word, steno_span_length

    if commit and expanded_word:
        FREQ.inc(expanded_word)


    steno_active = False
    typed_buffer = ""
    expanded_word = ""
    steno_span_length = 0
    cycle.clear()
    cancel_timer()

# ================= KEY HANDLER =================

def on_key(event):
    global steno_active, typed_buffer, steno_span_length, expanded_word

    if suppress:
        return

    if event.event_type != "down":
        return

    key = event.name

    # -------- Trigger --------
    if key == STENO_TRIGGER:
        steno_active = True
        typed_buffer = ""
        expanded_word = ""
        steno_span_length = 1  # the ';'
        cycle.clear()
        cancel_timer()
        return

    if not steno_active:
        return

    if not (key.isalpha() or key in CONTROL_KEYS):
        return

    # -------- Cycle --------
    if key in ("right", "right arrow"):
        if cycle.active:
            next_word = cycle.next()
            if next_word:
                replace_word(next_word)
        return

    # -------- Commit --------
    if key in ("space", "enter"):
        reset_state(commit=True)
        return

    # -------- Edit --------
    if key == "backspace":
        if steno_span_length > 0:
            steno_span_length -= 1
        if typed_buffer:
            typed_buffer = typed_buffer[:-1]
        expanded_word = ""
        cancel_timer()
        cycle.clear()
        return

    # -------- Alphabetic --------
    if len(key) == 1 and key.isalpha():
        typed_buffer += key.lower()
        steno_span_length += 1
        expanded_word = ""
        cycle.clear()
        schedule_expand()

# ================= START =================

keyboard.hook(on_key)

print("Steno engine running.")
print(f"Use '{STENO_TRIGGER}' to start a steno chord.")
print("Press ESC to quit.\n")

keyboard.wait("esc")
