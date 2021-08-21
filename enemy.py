import random

import pygame

map_width = 241
map_height = 18

enemies = []

vec = pygame.math.Vector2


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 120
        self.original_image = pygame.Surface((self.width, self.height))
        self.original_image.fill((255, 0, 0))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.midbottom = self.pos

    def update(self):
        self.acc = vec(0, 1.95)
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        if self.rect.bottom > pygame.display.get_surface().get_size()[1]:
            self.rect.bottom = pygame.display.get_surface().get_size()[1]


def create_enemies(num_of_enemies):

    lower_bound = 1000
    upper_bound = 1100

    for enemy in range(num_of_enemies):

        left = random.randrange(lower_bound, upper_bound)
        e = Enemy(left, 60)

        lower_bound = e.rect.right + random.randrange(50, 200) * 5
        upper_bound = lower_bound + 100

        enemies.append(e)
