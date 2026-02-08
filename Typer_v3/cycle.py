# cycle.py
from Typer_v3.frequency import FREQ

class CycleState:
    def __init__(self):
        #self.matches = []
        self.words = []
        self.index = 0
        self.active = False

    def reset(self, words): #matches
        # sort by frequency (descending)
        #self.matches = sorted(
        #    matches,
        #    key=lambda w: FREQ.get(w),
        #    reverse=True
        #)
        self.words = list(words)
        self.index = 0
        self.active = True

    '''
    def next(self):
        #if not self.matches:
        #    return None
        #self.index = (self.index + 1) % len(self.matches)
        #return self.current()
        if not self.active or not self.words:
            return None
        self.index += 1
        if self.index >= len(self.words):
            return None
        return self.words[self.index]
    '''

    def next(self):
        if not self.active or not self.words:
            return None
        self.index = (self.index + 1) % len(self.words)
        return self.words[self.index]

    def current(self):
        if not self.active or not self.words:
            return None
        return self.words[self.index]


    def extend(self, new_words):
        self.words.extend(new_words)

    def clear(self):
        #self.matches = []
        self.words = []
        self.index = 0
        self.active = False
