import pygame
from pygame.locals import *
import json
import enemy

m = open("levels.json",)
maps = json.load(m)

tile_maps = []

for map in maps["levels"]:
    tile_maps.append(map)


map_width = 241
map_height = 18

tiles = []

switch = {
    1: (0, 0, 61, 61),
    2: (61, 0, 61, 61),
    3: (122, 0, 61, 61),
    4: (0, 61, 61, 61),
    5: (61, 61, 61, 61),
    6: (122, 61, 61, 61),
    7: (0, 122, 61, 61),
    8: (61, 122, 61, 61),
    9: (122, 122, 61, 61),
    10: (183, 0, 61, 61),
    11: (183, 61, 61, 61),
    12: (183, 122, 61, 61),
    13: (0, 183, 61, 61),
    14: (61, 183, 61, 61),
    15: (122, 183, 61, 61),
    16: (183, 183, 61, 61),
    17: (244, 0, 61, 61),
    18: (305, 0, 61, 61),
    19: (244, 61, 61, 61),
    20: (305, 61, 61, 61)
}

level_num = 0


class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # Get sprite from spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image


class Level:

    def __init__(self, tile_map: list):
        self.tile_map = tile_map
        self.spritesheet = SpriteSheet("assets/" + str(level_num) + "/tileset.png")

        for y in range(map_height):

            for x in range(map_width):
                # Creates tiles for everything except open air
                if self.tile_map[y * map_width + x] != 0:

                    switcher = switch.get(self.tile_map[y * map_width + x], (255, 0, 0))
                    tile = Tile(x * map_width, y * map_height, self.spritesheet.get_image(switcher[0], switcher[1], switcher[2], switcher[3]))
                    tiles.append(tile)
                    
    def clear(self):
        tiles.clear()


class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, texture):
        pygame.sprite.Sprite.__init__(self)
        self.tile_width = 61
        self.tile_height = 61
        self.original_image = texture
        self.image = self.original_image
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x * (self.tile_width / map_width)
        self.rect.y = y * (self.tile_height / map_height)
        self.original_rect = self.rect.copy()

