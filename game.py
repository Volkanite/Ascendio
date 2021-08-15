import pygame
from pygame.locals import *

import levels
import player

FPS = 30

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((0, 0), FULLSCREEN)
pygame.display.set_caption("Ascendio")
logo = pygame.image.load('assets/logo.png')
logo.set_colorkey((255, 0, 255))
pygame.display.set_icon(logo)

clock = pygame.time.Clock()
pygame.key.set_repeat(FPS)

# Creates a new level
level = levels.Level(levels.tile_maps[levels.level_num])

tiles = pygame.sprite.Group()
entities = pygame.sprite.Group()

for tile in levels.tiles:
    tiles.add(tile)

playable = player.Player()
entities.add(playable)


def move_camera():

    if playable.rect.right >= pygame.display.get_surface().get_size()[0] / 2:

        if playable.acc.x > 0:

            playable.pos.x -= int(abs(playable.speed * playable.acc.x))

            for tile in tiles:
                tile.rect.x -= int(abs(playable.speed * playable.acc.x))

    elif playable.rect.left < pygame.display.get_surface().get_size()[0] / 3:

        if playable.acc.x < 0:

            playable.pos.x += int(abs(playable.speed * playable.acc.x))

            for tile in tiles:
                tile.rect.x += int(abs(playable.speed * playable.acc.x))


def update():
    tiles.update()
    entities.update()
    collided_x = False
    move_camera()

    # Player collision goes here
    if playable.rect.bottom > pygame.display.get_surface().get_size()[1]:
        playable.rect.bottom = pygame.display.get_surface().get_size()[1]
        playable.acc.y = 0

    for ti in levels.tiles:

        # Put X Axis Collision Here
        if ti.rect.colliderect(playable.rect.x, playable.rect.y, playable.width, playable.height):

            if playable.acc.x > 0 and ti.rect.top < playable.rect.top:
                playable.image.fill((0, 0, 255))
                collided_x = True
                playable.pos.x = playable.uncollided.x
                playable.pos.x -= abs(playable.speed * playable.acc.x)
            elif playable.acc.x < 0 and ti.rect.top < playable.rect.top:
                playable.image.fill((0, 255, 0))
                collided_x = True
                playable.pos.x = playable.uncollided.x
                playable.pos.x += abs(playable.speed * playable.acc.x)

        if ti.rect.colliderect(playable.rect.x, playable.rect.y, playable.width,
                               playable.height):

            # Y-axis Collision
            if playable.vel.y < 0 and ti.rect.bottom < playable.rect.bottom:
                playable.pos.y = ti.rect.bottom + playable.height
                playable.vel.y = 0

            elif playable.vel.y >= 0 and ti.rect.top > playable.rect.top:
                playable.pos.y = ti.rect.top
                playable.vel.y = 0

            playable.rect.midbottom = playable.pos

    if not collided_x:
        playable.uncollided = playable.pos


def draw():
    window.fill((255, 255, 255))
    tiles.draw(window)
    entities.draw(window)


running = True

while running:

    for event in pygame.event.get():

        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Tests if the player is standing on solid ground
                playable.rect.y += 1
                hits = pygame.sprite.spritecollide(playable, tiles, False)
                playable.rect.y -= 1
                playable.jump(hits and (playable.rect.left > hits[0].rect.left or playable.rect.right < hits[0].rect.right))

    update()

    draw()

    # Update Display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
