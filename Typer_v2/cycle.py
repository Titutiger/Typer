# cycle.py

class CycleState:
    def __init__(self):
        self.matches = []
        self.index = 0
        self.active = False

    def reset(self, matches):
        self.matches = matches
        self.index = 0
        self.active = True

    def next(self):
        if not self.matches:
            return None
        self.index = (self.index + 1) % len(self.matches)
        return self.current()

    def current(self):
        if not self.matches:
            return None
        return self.matches[self.index]

    def clear(self):
        self.matches = []
        self.index = 0
        self.active = False
