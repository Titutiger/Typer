# output.py
from pynput.keyboard import Controller
import time

class StenoOutput:
    def __init__(self, typing_delay=0.05):
        self.keyboard = Controller()
        self.typing_delay = typing_delay

    def delete_previous(self, length):
        for _ in range(length + 1):
            self.keyboard.press('\b')
            self.keyboard.release('\b')
            time.sleep(self.typing_delay / 2)

    def type_word(self, word, delete_chars=0):
        if delete_chars > 0:
            self.delete_previous(delete_chars)
        for char in word:
            self.keyboard.press(char)
            self.keyboard.release(char)
            time.sleep(self.typing_delay)
        self.keyboard.press(' ')
        self.keyboard.release(' ')

    def replace_word(self, old_word_length, new_word):
        self.delete_previous(old_word_length)
        for char in new_word:
            self.keyboard.press(char)
            self.keyboard.release(char)
            time.sleep(self.typing_delay)
        self.keyboard.press(' ')
