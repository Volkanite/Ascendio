import pygame
from pygame.locals import *

tile_maps = [
    [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ],
    [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 1, 1, 1, 1, 0, 1, 0,
        0, 1, 1, 1, 0, 0, 1, 0, 1, 0,
        0, 0, 0, 1, 1, 0, 1, 1, 1, 0,
        0, 1, 1, 1, 0, 0, 0, 0, 1, 0,
        0, 1, 0, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 0, 0, 1, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 0, 1, 1, 0,
        0, 0, 1, 0, 0, 1, 1, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
]

map_width = 10
map_height = 10

tiles = []

switch = [
    {   # rgb values
        1: (36, 36, 36)
    },
    {
        1: (255, 205, 205)
    }
]

level_num = 0


class Level:

    def __init__(self, tile_map: list):
        self.tile_map = tile_map

        for y in range(map_width):

            for x in range(map_height):
                # Creates tiles for everything except open air
                if self.tile_map[y * map_width + x] != 0:
                    tile = Tile(x * map_width, y * map_height, switch[level_num].get(self.tile_map[y * map_width + x], (120, 120, 120)))
                    tiles.append(tile)


class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, texture):
        pygame.sprite.Sprite.__init__(self)
        self.tile_width = 40
        self.tile_height = 40
        self.texture = texture
        self.original_image = pygame.Surface((self.tile_width, self.tile_height))
        self.original_image.fill(self.texture)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x * (self.tile_width / map_width)
        self.rect.y = y * (self.tile_height / map_height)
