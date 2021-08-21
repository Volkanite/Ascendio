import pygame

vec = pygame.math.Vector2


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 36
        self.height = 18
        self.original_image = pygame.image.load("assets/bullet.png").convert()
        self.original_image.set_colorkey((255, 0, 255))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.direction = 0
        self.pos = vec(x, y)
        self.vel = 0

    def update(self):
        self.vel += self.speed * self.direction
        self.pos.x += self.vel
        self.rect.midleft = self.pos
