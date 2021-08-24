import random

import pygame
import levels

map_width = 241
map_height = 18

enemies = []

vec = pygame.math.Vector2


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 72
        self.height = 120
        self.spritesheet = levels.SpriteSheet("assets/agents/characters.png")
        self.load_images()
        self.original_image = self.idle_frames[0]
        self.original_image.set_colorkey((255, 0, 255))
        self.mini_img = pygame.transform.scale(self.original_image, (15, 25))
        self.mini_img.set_colorkey((255, 0, 255))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.midbottom = self.pos
        self.original_rect = self.rect.copy()

        self.last_update = 0
        self.current_frame = 0

        self.health = 100

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0, 240, 72, 120),
                            self.spritesheet.get_image(72, 240, 72, 120)]

    def update(self):
        self.animate()
        self.acc = vec(0, 1.95)
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        if self.rect.bottom > pygame.display.get_surface().get_size()[1]:
            self.rect.bottom = pygame.display.get_surface().get_size()[1]

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.original_image = self.idle_frames[self.current_frame]
            self.original_image.set_colorkey((255, 0, 255))
            self.image = self.original_image


def create_enemies(num_of_enemies):

    lower_bound = 1000
    upper_bound = 1100

    for enemy in range(num_of_enemies):

        left = random.randrange(lower_bound, upper_bound)
        e = Enemy(left, 60)

        lower_bound = e.rect.right + random.randrange(50, 200) * 5
        upper_bound = lower_bound + 100

        enemies.append(e)
