import pygame
from pygame.locals import *
from optparse import OptionParser

import levels
import player


# Game Options
parser = OptionParser()
parser.add_option('-w', '--windowed', dest='windowed', help='Runs the game in windowed mode', default=None)
parser.add_option('-f', '--fps', dest='fps', help='Set frame rate', default=30)

pygame.init()
pygame.mixer.init()

(options, args) = parser.parse_args()
FPS = int(options.fps)

if (options.windowed):
    window = pygame.display.set_mode((1280, 720))
else:
    window = pygame.display.set_mode((0, 0), FULLSCREEN) 

pygame.display.set_caption("Ascendio")
logo = pygame.image.load('assets/logo.png')
logo.set_colorkey((255, 0, 255))
pygame.display.set_icon(logo)
font_name = pygame.font.match_font('arial')

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
        playable.jumping = False

    for ti in levels.tiles:

        # Put X Axis Collision Here
        if ti.rect.colliderect(playable.rect.x, playable.rect.y, playable.width, playable.height):

            if playable.acc.x > 0 and ti.rect.top - playable.height * 2 / 3 < playable.rect.top:
                collided_x = True
                playable.pos.x = playable.uncollided.x
                playable.pos.x -= abs(playable.speed * playable.acc.x)

            elif playable.acc.x < 0 and ti.rect.top - playable.height * 2 / 3 < playable.rect.top:
                collided_x = True
                playable.pos.x = playable.uncollided.x
                playable.pos.x += abs(playable.speed * playable.acc.x)

            playable.rect.midbottom = playable.pos

        if ti.rect.colliderect(playable.rect.x, playable.rect.y, playable.width,
                               playable.height):

            # Y-axis Collision
            if playable.vel.y < 0 and ti.rect.bottom < playable.rect.bottom:
                playable.pos.y = ti.rect.bottom + playable.height
                playable.vel.y = 0

            elif playable.vel.y >= 0 and ti.rect.top > playable.rect.top:
                playable.pos.y = ti.rect.top
                playable.vel.y = 0
                playable.jumping = False

            playable.rect.midbottom = playable.pos

    if not collided_x:
        playable.uncollided = playable.pos


def draw():
    window.fill((255, 255, 255))
    tiles.draw(window)
    entities.draw(window)
    
    
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rec = text_surface.get_rect()
    text_rec.midtop = (x, y)
    surf.blit(text_surface, text_rec)
    return y

    
def draw_menu():

    display_width = pygame.display.get_surface().get_size()[0]
    display_height = pygame.display.get_surface().get_size()[1]
    line_spacing = 30
    
    window.fill((0, 0, 0))
    draw_text(window, "Ascendio", 64, display_width / 2, display_height / 4)
    y = draw_text(window, "W A S D to move", 22, display_width / 2, display_height / 2)
    y = draw_text(window, "Space to jump", 22, display_width / 2, y + line_spacing)
    draw_text(window, "LMB to fire", 22, display_width / 2, y + line_spacing)       
    draw_text(window, "Press any key to start game", 18, display_width / 2, display_height * 3 / 4)
    
    pygame.display.flip()
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 2 # Quit
            
        if event.type == pygame.KEYUP:
            return 1 # Start Game
                
    return 0 # Keep running menu


running = True
playing = False


while running:

    # Menu screen
    while not playing:
        playing = draw_menu()
        
    if playing == 2:
        running = False
    
    if playing == 1:
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


def quit_game():
    pygame.quit()
