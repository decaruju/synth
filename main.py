import pygame
import pygame.midi
import time
import pyaudio
import numpy as np

from synth import Synth

p = pyaudio.PyAudio()

stream = p.open(format=2,
                channels=1,
                rate=44100,
                output=True,
                output_device_index=0
                )

RATE = 44100
NOTE = 440
NOTE_LENGTH = 10

pygame.init()
pygame.midi.init()

synth = Synth()

running = True
screen = pygame.display.set_mode((240,180))
input = pygame.midi.Input(3)
for index in range(pygame.midi.get_count()):
    print(pygame.midi.get_device_info(index))


controls = {
    1: {'name': 'attack', 'max': 100000},
    2: {'name': 'decay', 'max': 100000},
    3: {'name': 'sustain', 'max': 1},
    4: {'name': 'release', 'max': 100000},
}
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for event in input.read(100):
        if event[0][0] == 128:
            synth.unpress(pygame.midi.midi_to_frequency(event[0][1]))
        if event[0][0] == 144:
            synth.press(pygame.midi.midi_to_frequency(event[0][1]))
        if event[0][0] == 176:
            if event[0][1] in controls:
                control = controls[event[0][1]]
                setattr(synth, control['name'], event[0][2]/128*control['max'])
        print(event)

    data = synth.data().astype('int32')
    stream.write(data, exception_on_underflow=False)

stream.stop_stream()
stream.close()

p.terminate()
