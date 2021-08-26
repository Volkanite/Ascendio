import pygame
from pygame.locals import *
import levels

# Alias for Vector2
vec = pygame.math.Vector2


friction = -0.09
gravity = 1


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 120
        self.spritesheet = levels.SpriteSheet("assets/agents/characters.png")
        self.load_images()
        self.original_image = self.idle_frames[0]
        self.original_image.set_colorkey((255, 0, 255))
        self.image = self.original_image
        self.mini_img = pygame.transform.scale(self.original_image, (15, 25))
        self.mini_img.set_colorkey((255, 0, 255))
        self.original_rect = self.image.get_rect()
        self.rect = self.original_rect
        self.pos = vec(self.width, self.height * 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = 18
        self.uncollided = self.pos
        self.agent_num = 0

        self.walking = False
        self.jumping = False
        self.firing = False
        self.current_frame = 0
        self.firing_frame = 0
        self.last_update = 0
        self.lives = 3
        self.start_time = pygame.time.get_ticks()
        self.end_time = 0

        self.health = 100

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0, 120, 60, 120),
                            self.spritesheet.get_image(60, 120, 60, 120)]

        self.jumping_frames = [self.spritesheet.get_image(120, 120, 72, 120),
                               pygame.transform.flip(self.spritesheet.get_image(120, 120, 72, 120), True, False)]

        self.walking_frames_r = [self.spritesheet.get_image(0, 0, 60, 120),
                               self.spritesheet.get_image(60, 0, 60, 120),
                               self.spritesheet.get_image(120, 0, 60, 120),
                               self.spritesheet.get_image(180, 0, 75, 120),
                               self.spritesheet.get_image(255, 0, 75, 120)]

        self.walking_frames_l = []

        self.firing_frames_r = [self.spritesheet.get_image(192, 120, 78, 120),
                                self.spritesheet.get_image(270, 120, 66, 120)]

        self.firing_frames_l = []

        for frame in self.walking_frames_r:
            self.walking_frames_l.append(pygame.transform.flip(frame, True, False))

        for frame in self.firing_frames_r:
            self.firing_frames_l.append(pygame.transform.flip(frame, True, False))
    
    def reset(self):
        self.rect = self.original_rect
        self.pos = vec(self.width, self.height * 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.health = 100
        
    def jump(self, able):
        if able:
            self.vel.y = -23
            self.jumping = True

    def update(self):
        # Sets acceleration values
        self.animate()
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

    def animate(self):
        now = pygame.time.get_ticks()

        if self.acc.x != 0:
            self.walking = True
        else:
            self.walking = False

        # Firing Animation
        if self.firing:

            if now - self.last_update > 90:
                self.last_update = now
                self.firing_frame = (self.firing_frame + 1) % len(self.firing_frames_l)

                if (self.firing_frame + 1) % len(self.firing_frames_l) == 0:
                    self.firing = False

                if self.acc.x >= 0:
                    self.original_image = self.firing_frames_r[self.firing_frame]
                    self.original_image.set_colorkey((255, 0, 255))

                else:
                    self.original_image = self.firing_frames_l[self.firing_frame]
                    self.original_image.set_colorkey((255, 0, 255))

                self.width = self.original_image.get_width()
                self.height = self.original_image.get_height()
                self.image = self.original_image

        # Walking Animation
        if self.walking and not self.jumping:
            if now - self.last_update > 90:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)

                if self.acc.x > 0:
                    self.original_image = self.walking_frames_r[self.current_frame]
                    self.original_image.set_colorkey((255, 0, 255))
                else:
                    self.original_image = self.walking_frames_l[self.current_frame]
                    self.original_image.set_colorkey((255, 0, 255))

                self.width = self.original_image.get_width()
                self.height = self.original_image.get_height()
                self.image = self.original_image

        if self.jumping:

            if self.acc.x < 0:
                self.original_image = self.jumping_frames[1]
                self.original_image.set_colorkey((255, 0, 255))
            else:
                self.original_image = self.jumping_frames[0]
                self.original_image.set_colorkey((255, 0, 255))

            self.width = self.original_image.get_width()
            self.height = self.original_image.get_height()
            self.image = self.original_image

        # Idle Animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                self.original_image = self.idle_frames[self.current_frame]
                self.original_image.set_colorkey((255, 0, 255))
                self.width = self.original_image.get_width()
                self.height = self.original_image.get_height()
                self.image = self.original_image


