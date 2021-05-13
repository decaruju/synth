from abc import ABC, abstractmethod

import numpy as np


NUMBER_OF_SAMPLES = 10000
SAMPLE_RATE = 44100

class Signal(ABC):
    def __init__(self):
        self.age = 0

    def tick(self):
        data = self.data()
        self.age += NUMBER_OF_SAMPLES
        return data


class Enveloppe(Signal):
    def __init__(self, attack, decay, sustain, release, velocity):
        super().__init__()
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.velocity = velocity
        self.last_value = 0
        self.pressed = True

    def data(self):
        if self.pressed:
            full_enveloppe = np.concatenate((np.linspace(0, self.velocity, self.attack), np.linspace(self.velocity, self.sustain, self.decay), np.full(self.age + NUMBER_OF_SAMPLES, self.sustain)))
            data = full_enveloppe[self.age:self.age+NUMBER_OF_SAMPLES]
            self.last_value = data[-1]
            return data
        else:
            print(self.release)
            full_enveloppe = np.concatenate((np.linspace(self.last_value, 0, self.release), np.full(self.age+NUMBER_OF_SAMPLES, 0)))
            data = full_enveloppe[self.age:self.age+NUMBER_OF_SAMPLES]
            self.last_value = data[-1]
            return data

    def is_dead(self):
        return not self.pressed and self.last_value == 0

    def unpress(self):
        self.pressed = False
        self.age = 0


class Note(Signal):
    def __init__(self, frequency, enveloppe):
        super().__init__()
        self.frequency = frequency
        self.enveloppe = enveloppe
        self.pressed = True

    def release(self):
        self.pressed = False
        self.enveloppe.unpress()

    def is_dead(self):
        return self.enveloppe.is_dead()

    def data(self):
        enveloppe = self.enveloppe.tick()
        return enveloppe*np.sin(np.linspace(self.age/SAMPLE_RATE, (self.age+NUMBER_OF_SAMPLES)/SAMPLE_RATE, NUMBER_OF_SAMPLES)*self.frequency*2*np.pi)

