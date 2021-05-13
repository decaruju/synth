import numpy as np
from note import Note, Enveloppe, NUMBER_OF_SAMPLES

default_enveloppe_args = { 'attack': 10000, 'decay': 2000, 'sustain': 0.8, 'release': 100000 }

class Synth:
    def __init__(self):
        self.notes = {}
        self.attack = 10000
        self.decay = 2000
        self.sustain = 0.8
        self.release = 10000

    def data(self):
        if len(self.notes) == 0:
            return np.zeros(NUMBER_OF_SAMPLES)
        notes = np.array([note.tick() for note in self.notes.values()])
        data = np.sum(notes, axis=0)/4
        self.notes = {key: note for key, note in self.notes.items() if not note.is_dead()}
        return data*(2**31-1)

    def press(self, note_value, velocity=0.8):
        enveloppe = Enveloppe(attack=int(self.attack), decay=int(self.decay), sustain=self.sustain, release=int(self.release), velocity=velocity)
        self.notes[note_value] = Note(note_value, enveloppe)

    def unpress(self, note_value):
        if note_value in self.notes:
            self.notes[note_value].release()
