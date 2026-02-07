# input.py (partial)
from pynput import keyboard
from threading import Timer

class StenoInput:
    def __init__(self, chord_callback, special_key_callback=None, chord_timeout=0.1):
        self.pressed_keys = set()
        self.chord_callback = chord_callback
        self.special_key_callback = special_key_callback
        self.chord_timeout = chord_timeout
        self.timer = None

    def on_press(self, key):
        try:
            if key.char:
                self.pressed_keys.add(key.char.lower())
        except AttributeError:
            name = str(key).replace('Key.', '').lower()
            if name == 'right':
                if self.special_key_callback:
                    self.special_key_callback('right')
                return
            self.pressed_keys.add(name)
        if self.timer:
            self.timer.cancel()

    def on_release(self, key):
        if key == keyboard.Key.esc:
            return False
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.chord_timeout, self.process_chord)
        self.timer.start()

    def process_chord(self):
        if self.pressed_keys:
            self.chord_callback(self.pressed_keys.copy())
            self.pressed_keys.clear()

    def start_listening(self):
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        ) as listener:
            listener.join()
