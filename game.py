import pygame
from pygame.locals import *
from optparse import OptionParser

import levels
import player
import enemy
import sounds
import bullet


# Game Options
parser = OptionParser()
parser.add_option('-w', '--windowed', dest='windowed', action='store_true', help='Runs the game in windowed mode', default=None)
parser.add_option('-f', '--fps', dest='fps', help='Set frame rate', default=None)

pygame.init()
pygame.mixer.init()

(options, args) = parser.parse_args()
FPS = 30
show_fps = False

if options.fps:
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
timer_animate_min = 24
timer_animate_max = 100
kills = 0

on_screen = pygame.sprite.Group()
tiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
entities = pygame.sprite.Group()
bullets = pygame.sprite.Group()

level = None
playable = None
last_tile = None


# Creates a new level
def create_level():
    global level
    global last_tile
    
    on_screen.empty()
    tiles.empty()
    enemies.empty()
    entities.empty()
    
    if level:
        level.clear()
        
    level = levels.Level(levels.tile_maps[levels.level_num])
    
    enemy.enemies.clear()
    enemy.create_enemies(19)

    for e in enemy.enemies:
        enemies.add(e)

    for tile in levels.tiles:
        tiles.add(tile)
        
    # get last tile for level progress
    last_tile = levels.tiles[-1]

        
# Resets the tiles in a level
def reset_level():

    for tile in tiles:
        tile.rect = tile.original_rect.copy()

    for e in enemies:
        e.pos.x = e.original_rect.x
        e.rect.midbottom = e.pos



# Creates a new player
def create_player():
    global playable
    
    playable = player.Player()
    entities.add(playable)


def move_camera():

    if playable.rect.right >= pygame.display.get_surface().get_size()[0] / 2:

        playable.pos.x -= int(abs(playable.speed * 0.55 + 1))

        for e in enemies:
            e.pos.x -= int(abs(playable.speed * 0.55 + 1))

        for tile in tiles:
            tile.rect.x -= int(abs(playable.speed * 0.55 + 1))

    elif playable.rect.left < pygame.display.get_surface().get_size()[0] / 3:

        playable.pos.x += int(abs(playable.speed * 0.55 + 1))

        for e in enemies:
            e.pos.x += int(abs(playable.speed * 0.55 + 1))

        for tile in tiles:
            tile.rect.x += int(abs(playable.speed * 0.55 + 1))

    if playable.rect.top <= pygame.display.get_surface().get_size()[1] / 4:

        playable.pos.y += int(abs(playable.vel.y + 0.5 * playable.acc.y))

        for e in enemies:
            e.rect.y += int(abs(playable.vel.y + 0.5 * playable.acc.y))

        for tile in tiles:
            tile.rect.y += int(abs(playable.vel.y + 0.5 * playable.acc.y))

    elif pygame.display.get_surface().get_size()[1] * 7 / 8 < playable.rect.bottom < \
            pygame.display.get_surface().get_size()[1] * 15 / 16:

        playable.pos.y -= int(abs(playable.vel.y))

        for e in enemies:
            e.rect.y -= int(abs(playable.vel.y))

        for tile in tiles:
            tile.rect.y -= int(abs(playable.vel.y))


def update():
    tiles.update()
    enemies.update()
    entities.update()
    bullets.update()
    collided_x = False
    move_camera()

    on_screen.empty()

    for b in bullets:
        if b.rect.right < 0 or b.rect.left > pygame.display.get_surface().get_size()[0]:
            b.kill()

        for e in enemies:

            if b.rect.colliderect(e.rect.x, e.rect.y, e.width, e.height):
                b.kill()
                e.health -= 40

                if e.health < 0:
                    global kills
                    e.kill()
                    kills += 1

    for tile in tiles:
        if tile.rect.right >= 0 and tile.rect.left <= pygame.display.get_surface().get_size()[0]:
            if tile.rect.bottom >= 0 and tile.rect.top <= pygame.display.get_surface().get_size()[1]:
                on_screen.add(tile)

    # Player collision goes here
    if playable.rect.bottom > pygame.display.get_surface().get_size()[1]:
        playable.lives -= 1
        playable.reset()
        reset_level()

    for e in enemies:

        for ti in tiles:

            if ti.rect.colliderect(e.rect.x, e.rect.y, e.width, e.height):

                if e.vel.y < 0 and ti.rect.bottom < e.rect.bottom:
                    e.pos.y = ti.rect.bottom - e.height
                    e.vel.y = 0

                elif e.vel.y >= 0 and ti.rect.top > e.rect.top:
                    e.pos.y = ti.rect.top
                    e.vel.y = 0

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

        if ti.rect.colliderect(playable.rect.x, playable.rect.y, playable.width, playable.height):

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
    
    # check for end of level (kinda)
    if playable.rect.x > last_tile.rect.x - 200:
        global game_over
        game_over = 1
        if not playable.end_time:
            playable.end_time = pygame.time.get_ticks()


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

    window.blit(fps, (10, 10))


def draw():
    window.fill((255, 255, 255))

    on_screen.draw(window)
    enemies.draw(window)
    entities.draw(window)
    bullets.draw(window)
    
    draw_hud()

    if show_fps:
        draw_frame_rate()


def draw_hud():
    window_width = pygame.display.get_surface().get_size()[0]
    
    draw_lives(window, window_width - 100, 5, playable.lives, playable.mini_img)
    # draw_health_bar()
    
    # timer
    global timer_animate_min
    
    if playable.end_time:
        if timer_animate_min < timer_animate_max:
            timer_animate_min += 1
            
        draw_score(window, 
            window_width / 2, 
            125, 
            timer_animate_min)   
            
    draw_timer(window, 
        window_width / 2, 
        5, 
        timer_animate_min,
        playable.end_time if playable.end_time else pygame.time.get_ticks() - playable.start_time,
        playable.end_time)

    # kills
    draw_kills(window, 50, 5, enemy.enemies[0].mini_img)


def draw_score(surface, x, y, size):
    if kills:
        score = int((kills * 1000) / int(round(playable.end_time / 1000, 0)) * 10)
    else:
        score = int(500 / int(round(playable.end_time / 1000, 0)) * 10)
        
    draw_text(surface, str(score) + " points", size, x, y, (0, 0, 0))
    
    
def draw_timer(surface, x, y, size, time, unit):
    timer_string = str(int(round(time / 1000, 0)))
    
    if unit:
        timer_string += " s"
        
    draw_text(surface, timer_string, size, x, y, (0, 0, 0))
    
    
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 20 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        
        
def draw_kills(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.x = x
    img_rect.y = y
    surf.blit(img, img_rect)
    draw_text(window, "x " + str(kills), 24, x + 35, 5, (0,0,0))

        
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rec = text_surface.get_rect()
    text_rec.midtop = (x, y)
    surf.blit(text_surface, text_rec)
    return y


menu = sounds.Sound("menu", sounds.sound_lengths["menu"], 1)


def draw_menu():
    display_width = pygame.display.get_surface().get_size()[0]
    display_height = pygame.display.get_surface().get_size()[1]
    line_spacing = 30
    color = (255, 255, 255)

    menu.play_sound()

    window.fill((0, 0, 0))
    draw_text(window, "Ascendio", 64, display_width / 2, display_height / 4, color)
    y = draw_text(window, "A D to move", 22, display_width / 2, display_height / 2, color)
    y = draw_text(window, "Space to jump", 22, display_width / 2, y + line_spacing, color)
    y = draw_text(window, "LMB to fire", 22, display_width / 2, y + line_spacing, color)
    draw_text(window, "Esc to exit", 22, display_width / 2, y + line_spacing, color)
    draw_text(window, "Press any key to start game", 18, display_width / 2, display_height * 3 / 4, color)

    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 2  # Quit

        if event.type == pygame.KEYUP:
            if event.key != pygame.K_ESCAPE:
                menu.stop_playing()
                level = None
                create_level()
                create_player()
                return 1  # Start Game

            elif event.key == pygame.K_ESCAPE:
                return 2

    return 0  # Keep running menu


running = True
playing = 0
game_over = 0

level_music = sounds.Sound(str(levels.level_num), sounds.sound_lengths[str(levels.level_num)], 100)
jump_sound = sounds.Sound("jump", sounds.sound_lengths["jump"], 1)
jump_sound.set_volume(0.3)


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

                    if hits and (playable.rect.left > hits[0].rect.left or playable.rect.right < hits[0].rect.right):
                        jump_sound.play_sound()

                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    playable.firing = True
                    b = bullet.Bullet(playable.rect.right, playable.rect.top + 30)
                    if playable.acc.x >= 0:
                        b.direction = 1

                    elif playable.acc.x < 0:
                        b.direction = -1
                        b.image = pygame.transform.flip(b.original_image, True, False)
                        b.pos.x = playable.rect.left

                    bullets.add(b)
        
        if playable.lives == 0:
            playing = False  # show menu screen

        update()

        draw()
        level_music.play_sound()

        # Update Display
        pygame.display.update()
        clock.tick(FPS)


def quit_game():
    pygame.quit()
