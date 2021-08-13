import pygame
from pygame.locals import *

import levels
import player

RESOLUTION = (400, 400)
FPS = 30

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Ascendio")

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


def update():
    tiles.update()
    entities.update()

    # Player collision goes here


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
                playable.rect.x += 1
                hits = pygame.sprite.spritecollide(playable, tiles, False)
                playable.rect.x -= 1
                playable.jump(hits)

    update()

    draw()

    # Update Display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
