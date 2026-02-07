# input.py
import keyboard
import threading

from Typer_v2.mapping import WORD_MAP, normalize
from Typer_v2.cycle import CycleState

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
steno_span_length = 0   # chars to delete (from ';' to cursor)

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
    global suppress
    suppress = True
    for _ in range(steno_span_length):
        keyboard.send("backspace")
    suppress = False


def replace_word(new_word):
    global expanded_word, steno_span_length

    delete_span()
    keyboard.write(new_word)

    expanded_word = new_word
    steno_span_length = len(new_word)


def try_expand():
    global expanded_word, steno_span_length

    if not steno_active:
        return

    if not typed_buffer or len(typed_buffer) > 4:
        return

    sig = normalize(typed_buffer)
    matches = WORD_MAP.get(sig)

    if not matches:
        return

    cycle.reset(matches)
    expanded_word = ""
    replace_word(matches[0])


def schedule_expand():
    global expand_timer
    cancel_timer()
    expand_timer = threading.Timer(EXPAND_DELAY, try_expand)
    expand_timer.start()


def reset_state():
    global steno_active, typed_buffer, expanded_word, steno_span_length
    steno_active = False
    typed_buffer = ""
    expanded_word = ""
    steno_span_length = 0
    cycle.clear()
    cancel_timer()

# ================= KEY HANDLER =================

def on_key(event):
    global steno_active, typed_buffer, steno_span_length

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
        reset_state()
        return

    # -------- Edit --------
    if key == "backspace":
        if typed_buffer:
            typed_buffer = typed_buffer[:-1]
            steno_span_length -= 1
        cancel_timer()
        cycle.clear()
        return

    # -------- Alphabetic --------
    if len(key) == 1 and key.isalpha():
        typed_buffer += key.lower()
        steno_span_length += 1
        cycle.clear()
        schedule_expand()

# ================= START =================

keyboard.hook(on_key)

print("Steno engine running.")
print(f"Use '{STENO_TRIGGER}' to start a steno chord.")
print("Press ESC to quit.\n")

keyboard.wait("esc")
