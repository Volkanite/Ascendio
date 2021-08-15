import pygame
from pygame.locals import *

# Alias for Vector2
vec = pygame.math.Vector2


friction = -0.09
gravity = 1


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 40
        self.height = 40
        self.original_image = pygame.Surface((self.width, self.height))
        self.original_image.fill((255, 0, 0))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = 8
        self.uncollided = self.pos

    def jump(self, able):
        if able:
            self.vel.y = -18

    def update(self):
        # Sets acceleration values
        self.acc = vec(0, 1.95 * gravity)
        key_state = pygame.key.get_pressed()

        if key_state[pygame.K_a]:
            self.acc.x = -0.55

        elif key_state[pygame.K_d]:
            self.acc.x = 0.55

        self.vel += self.acc
        self.pos.x += self.acc.x * self.speed
        self.pos.y += self.vel.y + 0.5 * self.acc.y

        self.rect.midbottom = self.pos
