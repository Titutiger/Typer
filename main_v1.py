"""

This is a python script to output a word by pressing all of it's letters at the same time.

"""

# main_v1.py
from Typer_v1.input import StenoInput
from Typer_v1.mapping import get_word_forms_from_chord
from Typer_v1.output import StenoOutput

current_word_forms = []
current_form_index = 0
current_word_length = 0  # length of currently typed word without trailing space

steno_output = StenoOutput()

def chord_received(chord):
    global current_word_forms, current_form_index, current_word_length
    word_forms = get_word_forms_from_chord(chord)
    if word_forms:
        current_word_forms = word_forms
        current_form_index = 0
        base_word = current_word_forms[current_form_index]
        print(f"Chord {chord} mapped to word form: {base_word}")
        steno_output.type_word(base_word, delete_chars=len(chord))
        current_word_length = len(base_word)
    else:
        print(f"Chord {chord} not mapped to any word.")
        current_word_forms = []
        current_form_index = 0
        current_word_length = 0

def special_key_received(key_name):
    global current_form_index, current_word_forms, current_word_length
    if key_name == 'right' and current_word_forms:
        # Cycle to next word form
        current_form_index = (current_form_index + 1) % len(current_word_forms)
        next_word = current_word_forms[current_form_index]
        print(f"Cycling to next form: {next_word}")
        steno_output.replace_word(current_word_length, next_word)
        current_word_length = len(next_word)

if __name__ == "__main__":
    steno_input = StenoInput(chord_received, special_key_received)
    print("Start stenography typing. Press Esc to exit.")
    steno_input.start_listening()

