import pygame
from pygame.locals import *

# Alias for Vector2
vec = pygame.math.Vector2


friction = -0.09
gravity = 1


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 20
        self.height = 20
        self.original_image = pygame.Surface((self.width, self.height))
        self.original_image.fill((255, 0, 0))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = vec(self.width / 2, self.height /2)
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        # self.hits = []
        self.uncollided = self.pos
    def jump(self, able):
        if able:
            self.vel.y = -18

    def update(self):
        # Sets acceleration values
        self.acc = vec(0, 1.95 * gravity)
        key_state = pygame.key.get_pressed()

        if key_state[pygame.K_a]:
            self.acc.x = -0.5

        elif key_state[pygame.K_d]:
            self.acc.x = 0.5

        self.acc.x += self.vel.x * friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
