import pygame
from pygame.locals import *
from optparse import OptionParser

import levels
import player
import sounds


# Game Options
parser = OptionParser()
parser.add_option('-w', '--windowed', dest='windowed', action='store_true', help='Runs the game in windowed mode', default=None)
parser.add_option('-f', '--fps', dest='fps', help='Set frame rate', default=None)

pygame.init()
pygame.mixer.init()

(options, args) = parser.parse_args()
FPS = 30
show_fps = False

if (options.fps):
    FPS = int(options.fps)
    show_fps = True

if options.windowed:
    window = pygame.display.set_mode((1280, 720))
else:
    window = pygame.display.set_mode((0, 0), FULLSCREEN)


pygame.display.set_caption("Ascendio")
logo = pygame.image.load('assets/logo.png')
logo.set_colorkey((255, 0, 255))
pygame.display.set_icon(logo)
font_name = pygame.font.match_font('arial')
font_fps = pygame.font.Font(font_name, 20)

clock = pygame.time.Clock()
pygame.key.set_repeat(FPS)
old_frame_rate = 0.0
new_frame_rate = 0.0

on_screen = pygame.sprite.Group()

tiles = pygame.sprite.Group()


# Creates a new level
def create_level():
    level = levels.Level(levels.tile_maps[levels.level_num])

    for tile in levels.tiles:
        tiles.add(tile)


entities = pygame.sprite.Group()

playable = player.Player()
entities.add(playable)


def move_camera():

    if playable.rect.right >= pygame.display.get_surface().get_size()[0] / 2:

        playable.pos.x -= int(abs(playable.speed * 0.55 + 1))

        for tile in tiles:
            tile.rect.x -= int(abs(playable.speed * 0.55 + 1))

    elif playable.rect.left < pygame.display.get_surface().get_size()[0] / 3:

        playable.pos.x += int(abs(playable.speed * 0.55 + 1))

        for tile in tiles:
            tile.rect.x += int(abs(playable.speed * 0.55 + 1))

    if playable.rect.top <= pygame.display.get_surface().get_size()[1] / 4:

        playable.pos.y += int(abs(playable.vel.y + 0.5 * playable.acc.y))

        for tile in tiles:
            tile.rect.y += int(abs(playable.vel.y + 0.5 * playable.acc.y))

    elif pygame.display.get_surface().get_size()[1] * 7 / 8 < playable.rect.bottom < \
            pygame.display.get_surface().get_size()[1] * 15 / 16:

        playable.pos.y -= int(abs(playable.vel.y ))

        for tile in tiles:
            tile.rect.y -= int(abs(playable.vel.y))


def update():
    tiles.update()
    entities.update()
    collided_x = False
    move_camera()

    on_screen.empty()

    for tile in tiles:
        if tile.rect.right >= 0 and tile.rect.left <= pygame.display.get_surface().get_size()[0]:
            if tile.rect.bottom >= 0 and tile.rect.top <= pygame.display.get_surface().get_size()[1]:
                on_screen.add(tile)

    # Player collision goes here
    if playable.rect.bottom > pygame.display.get_surface().get_size()[1]:
        playable.rect.bottom = pygame.display.get_surface().get_size()[1]
        playable.acc.y = 0
        playable.jumping = False

    for ti in on_screen:

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


def draw_frame_rate():
    # FPS calculation
    global old_frame_rate
    global new_frame_rate

    new_frame_rate = clock.get_fps()
    new_frame_rate = new_frame_rate * 0.1 + old_frame_rate * 0.9
    old_frame_rate = new_frame_rate

    if new_frame_rate > float(FPS) and new_frame_rate - float(FPS) < 1.6:
        new_frame_rate = float(FPS)

    fps = font_fps.render(str(int(new_frame_rate)), True, (255, 0, 0) if new_frame_rate < float(FPS - 5) else (0, 255, 0))

    window.blit(fps, (pygame.display.get_surface().get_size()[0] - 50, 10))


def draw():
    window.fill((255, 255, 255))

    on_screen.draw(window)
    entities.draw(window)

    if show_fps:
        draw_frame_rate()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rec = text_surface.get_rect()
    text_rec.midtop = (x, y)
    surf.blit(text_surface, text_rec)
    return y


menu = sounds.Sound("menu", sounds.sound_lengths["menu"], 100)


def draw_menu():
    display_width = pygame.display.get_surface().get_size()[0]
    display_height = pygame.display.get_surface().get_size()[1]
    line_spacing = 30

    menu.play_sound()

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
            return 2  # Quit

        if event.type == pygame.KEYUP:
            menu.stop_playing()
            create_level()
            return 1  # Start Game

    return 0  # Keep running menu


running = True
playing = False

level_music = sounds.Sound(str(levels.level_num), sounds.sound_lengths[str(levels.level_num)], 1700)

while running:

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
                    playable.jump(
                        hits and (playable.rect.left > hits[0].rect.left or playable.rect.right < hits[0].rect.right))

        update()

        draw()
        level_music.play_sound()

        # Update Display
        pygame.display.update()
        clock.tick(FPS)


def quit_game():
    pygame.quit()
