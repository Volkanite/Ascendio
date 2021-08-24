import pygame.mixer
import json

pygame.mixer.init()

s = open("sounds.json",)
snds = json.load(s)

sounds = {}
sound_lengths = {
    "menu": 17500,
    "jump": 453,
    "0": 22500
}

for key, value in snds.items():
    sounds[key] = pygame.mixer.Sound(value)


class Sound:

    def __init__(self, sound, length, iteration):
        self.sound = sound
        self.length = length
        self.iteration = iteration
        self.last_update = 0
        self.time_started = None

    def play_sound(self):

        if self.time_started is None:
            self.time_started = pygame.time.get_ticks()

        now = pygame.time.get_ticks()

        if self.last_update == 0 and now - self.last_update < self.length + self.time_started:
            sounds[self.sound].play()
            self.last_update = self.iteration

        if now - self.last_update - self.time_started > self.length:
            self.last_update = now
            self.time_started = 0
            sounds[self.sound].play()

    def stop_playing(self):
        sounds[self.sound].stop()
        
    def set_volume(self, value):
        sounds[self.sound].set_volume(value)
