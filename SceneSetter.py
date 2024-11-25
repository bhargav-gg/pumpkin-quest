import pygame
import sys
import os
import time

import images
import colors
import constants

import Button
from SpriteFactory import SpriteFactory

import random

CENTERED_LOGO_POS = []

FPS_CLOCK = None
SCREEN = None
CURSOR_RECT = None

HALLOWEEN_COMPLETE = False
THANKSGIVING_COMPLETE = False
CHRISTMAS_COMPLETE = False

current_scene = "credits"

def initialize():
    global CENTERED_LOGO_POS, FPS_CLOCK, SCREEN, CURSOR_RECT

    pygame.init()
    pygame.mouse.set_visible(False)

    if os.name == 'nt':
        import ctypes
        myappid = u'Pumpkin Quest' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    CENTERED_LOGO_POS = [(constants.WIDTH - images.LOGO.get_rect().size[0]) / 2, (constants.HEIGHT - images.LOGO.get_rect().size[1]) / 2]

    FPS_CLOCK = pygame.time.Clock()

    SCREEN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    SCREEN.fill(colors.BLACK)

    CURSOR_RECT = images.CURSOR.get_rect()

    pygame.display.set_caption("Pumpkin Quest")
    pygame.display.set_icon(images.LOGO_ICON)

def loadCreditScene():
    global current_scene
    time.sleep(1)

    for i in range(255):
        SCREEN.fill(colors.BLACK)
        images.LOGO.set_alpha(i)
        SCREEN.blit(images.LOGO, CENTERED_LOGO_POS)
        pygame.display.update()
        time.sleep(0.005)

    time.sleep(1)

    for i in range(255):
        SCREEN.fill(colors.BLACK)
        images.LOGO.set_alpha(255 - i)
        SCREEN.blit(images.LOGO, CENTERED_LOGO_POS)
        pygame.display.update()
        time.sleep(0.005)
    
    current_scene = "story"

def loadStoryScene(strings, next_scene):
    global current_scene

    story_font = pygame.font.SysFont("Cascadia Code", constants.WIDTH // 20)
    click_sound = pygame.mixer.Sound("media/click.mp3")

    for segment in strings:
        mouse_click = False
        while not mouse_click:
            SCREEN.fill(colors.BLACK)

            drawText(SCREEN, segment, colors.WHITE, (constants.WIDTH // 10, constants.HEIGHT // 10, constants.WIDTH // 10 * 8, constants.HEIGHT // 10 * 8), story_font)

            CURSOR_RECT.center = pygame.mouse.get_pos()
            SCREEN.blit(images.CURSOR, CURSOR_RECT)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_click = True
                    pygame.mixer.Sound.play(click_sound)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

            FPS_CLOCK.tick(constants.FPS)
    
    current_scene = next_scene

def loadMenuScene():
    global current_scene
    font = pygame.font.SysFont("Cascadia Code", constants.WIDTH // 20)

    title_font = pygame.font.SysFont("Cascadia Code", constants.WIDTH // 10)
    title = title_font.render("Pumpkin Quest", True, colors.WHITE)

    halloween_button = Button.Button(colors.ORANGE, colors.BLACK, (constants.WIDTH // 2) - (constants.WIDTH // 8), (constants.HEIGHT // 16) * 7, constants.WIDTH // 4, constants.HEIGHT // 8, font, "Halloween")
    thanksgiving_button = Button.Button(colors.BROWN, colors.GOLD, (constants.WIDTH // 2) - (constants.WIDTH // 8), (constants.HEIGHT // 16) * 10, constants.WIDTH // 4, constants.HEIGHT // 8, font, "Thanksgiving")
    christmas_button = Button.Button(colors.CHRISTMAS_RED, colors.CHRISTMAS_GREEN, (constants.WIDTH // 2) - (constants.WIDTH // 8), (constants.HEIGHT // 16) * 13, constants.WIDTH // 4, constants.HEIGHT // 8, font, "Christmas")
    secret_button = Button.Button(colors.WHITE, colors.BLACK, (constants.WIDTH // 2) - (constants.WIDTH // 8), constants.HEIGHT // 2, constants.WIDTH // 4, constants.HEIGHT // 8, font, "???")

    click_sound = pygame.mixer.Sound("media/click.mp3")

    """
    button_group = [halloween_button]

    if HALLOWEEN_COMPLETE:
        button_group.append(thanksgiving_button)
    
    if THANKSGIVING_COMPLETE:
        button_group.append(christmas_button)
    
    if CHRISTMAS_COMPLETE:
        button_group = [secret_button]
    """

    button_group = [halloween_button, thanksgiving_button, christmas_button]
    
    while current_scene == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                for button in button_group:
                    if button.isOver(pos):
                        if button.text == "Halloween":
                            current_scene = "halloween_story"
                            click_sound.play()
                        elif button.text == "Thanksgiving":
                            current_scene = "thanksgiving_story"
                            click_sound.play()
                        elif button.text == "Christmas":
                            current_scene = "christmas_story"
                            click_sound.play()
                        elif button.text == "???":
                            current_scene = "secret_story"
                            click_sound.play()
                
                break
        
        SCREEN.fill(colors.BLACK)

        for button in button_group:
            button.draw(SCREEN, colors.WHITE)
        
        SCREEN.blit(title, ((constants.WIDTH - title.get_width()) // 2, constants.HEIGHT // 16))
        
        CURSOR_RECT.center = pygame.mouse.get_pos()
        SCREEN.blit(images.CURSOR, CURSOR_RECT)

        pygame.display.update()
        FPS_CLOCK.tick(constants.FPS)

def loadHalloweenScene():
    global current_scene, HALLOWEEN_COMPLETE
    player = SpriteFactory.createSprite("Player", 0, 300, movement_speed=2)
    pumpkin = SpriteFactory.createSprite("Object", 60, 210, image_path="media/halloween_pumpkin.png")
    darkness = SpriteFactory.createSprite("Object", 0, 0, image_path="media/darkness.png")

    footstep_sound = pygame.mixer.Sound("media/footsteps.mp3")
    ding_sound = pygame.mixer.Sound("media/ding.mp3")

    text_frame_count = 0

    font = pygame.font.SysFont("Cascadia Code", constants.WIDTH // 20)

    hedges = pygame.sprite.Group()
    dirt = pygame.sprite.Group()

    walk_channel = pygame.mixer.Channel(0)

    pumpkin_acquired = False

    hedge_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    for i in range(len(hedge_map)):
        for j in range(len(hedge_map[i])):
            if hedge_map[i][j] == 1:
                hedge = SpriteFactory.createSprite("Object", j * 50, i * 50, image_path="media/HEDGE.png")
                hedges.add(hedge)
            elif hedge_map[i][j] == 0:
                dirt_block = SpriteFactory.createSprite("Object", j * 50, i * 50, image_path="media/DIRT.png")
                dirt.add(dirt_block)

    while current_scene == "halloween":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        old_rect = player.rect.copy()

        player.update(hedges)

        if not walk_channel.get_busy():
            walk_channel.play(footstep_sound)
        
        if old_rect == player.rect:
            walk_channel.stop()

        if pygame.sprite.collide_rect(player, pumpkin):
            pumpkin_acquired = True
            ding_sound.play()

            pumpkin.rect.x = -100
            pumpkin.rect.y = -100

        if player.rect.x >= constants.WIDTH - 25 and pumpkin_acquired:
            current_scene = "halloween_aftermath"
            HALLOWEEN_COMPLETE = True
            walk_channel.stop()
            ding_sound.play()
        
        SCREEN.fill(colors.BLACK)

        for dirt_block in dirt:
            SCREEN.blit(dirt_block.image, dirt_block.rect)

        for hedge in hedges:
            SCREEN.blit(hedge.image, hedge.rect)
        
        if not pumpkin_acquired:
            SCREEN.blit(pumpkin.image, pumpkin.rect)

        SCREEN.blit(player.image, player.rect)

        darkness.rect.center = player.rect.center
        SCREEN.blit(darkness.image, darkness.rect)

        if pumpkin_acquired and text_frame_count < 180:
            text_frame_count += 1
            drawText(SCREEN, "You found the pumpkin!", colors.WHITE, (constants.WIDTH // 2, (constants.HEIGHT // 8) * 7, constants.WIDTH // 10 * 8, constants.HEIGHT // 10 * 8), font)

        CURSOR_RECT.center = pygame.mouse.get_pos()
        SCREEN.blit(images.CURSOR, CURSOR_RECT)

        pygame.display.update()
        FPS_CLOCK.tick(constants.FPS)

def loadThanksgivingScene():
    global current_scene, THANKSGIVING_COMPLETE
    player = SpriteFactory.createSprite("Player", 0, 300, movement_speed=2)

    floorboards = pygame.image.load("media/floorboards.png")

    collision_group = pygame.sprite.Group()
    watcher_group = pygame.sprite.Group()

    ding_channel = pygame.mixer.Channel(0)
    ding_sound = pygame.mixer.Sound("media/ding.mp3")

    error_channel = pygame.mixer.Channel(1)
    error_sound = pygame.mixer.Sound("media/error.mp3")

    walk_channel = pygame.mixer.Channel(2)
    footstep_sound = pygame.mixer.Sound("media/wood_footsteps.mp3")

    pumpkin_collected = False
    pumpkin = SpriteFactory.createSprite("Object", 750, 300, image_path="media/thanksgiving_pumpkin.png")

    #0 = nothing
    #1 = table1
    #2 = table2
    #3 = table3
    #4 = chair1
    #5 = chair2
    #6 = chair3
    #7 = watcher (l/r)
    #8 = watcher (f/b)
    #Each cell represents a 25x25 square of the 800x600 screen
    level_grid = [
        [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 6, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 8, 0, 0, 0, 0, 0, 7, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 5, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 5, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 2, 0, 8, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 7, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 4, 0, 0],
        [0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0]
    ]

    for i in range(len(level_grid)):
        for j in range(len(level_grid[i])):
            if level_grid[i][j] == 1:
                table = SpriteFactory.createSprite("Object", j * 25, i * 25, image_path="media/table1.png")
                collision_group.add(table)
            elif level_grid[i][j] == 2:
                table = SpriteFactory.createSprite("Object", j * 25, i * 25, image_path="media/table2.png")
                collision_group.add(table)
            elif level_grid[i][j] == 3:
                table = SpriteFactory.createSprite("Object", j * 25, i * 25, image_path="media/table3.png")
                collision_group.add(table)
            elif level_grid[i][j] == 4:
                chair = SpriteFactory.createSprite("Object", j * 25, i * 25, image_path="media/chair1.png")
                collision_group.add(chair)
            elif level_grid[i][j] == 5:
                chair = SpriteFactory.createSprite("Object", j * 25, i * 25, image_path="media/chair2.png")
                collision_group.add(chair)
            elif level_grid[i][j] == 6:
                chair = SpriteFactory.createSprite("Object", j * 25, i * 25, image_path="media/chair3.png")
                collision_group.add(chair)
            elif level_grid[i][j] == 7:
                watcher = SpriteFactory.createSprite("Watcher", j * 25, i * 25, direction="left", threshold=random.randint(120, 300))
                watcher_group.add(watcher)           
            elif level_grid[i][j] == 8:
                watcher = SpriteFactory.createSprite("Watcher", j * 25, i * 25, direction="forward", threshold=random.randint(120, 300))
                watcher_group.add(watcher)  

    while current_scene == "thanksgiving":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        old_rect = player.rect.copy()
        
        player.update(collision_group)

        if pygame.sprite.collide_rect(player, pumpkin):
            pumpkin_collected = True
            ding_channel.play(ding_sound)
            pumpkin.rect.x = -100
            pumpkin.rect.y = -100


        if not walk_channel.get_busy():
            walk_channel.play(footstep_sound)
        
        if old_rect == player.rect:
            walk_channel.stop()
        
        SCREEN.fill(colors.BLACK)

        SCREEN.blit(floorboards, (0, 0))

        for watcher in watcher_group:
            watcher.update()
            SCREEN.blit(watcher.image, watcher.rect)
        
        for collision_object in collision_group:
            SCREEN.blit(collision_object.image, collision_object.rect)
        
        if not pumpkin_collected:
            SCREEN.blit(pumpkin.image, pumpkin.rect)
        
        SCREEN.blit(player.image, player.rect)

        if pumpkin_collected and player.rect.x <= 10:
            current_scene = "thanksgiving_aftermath"
            THANKSGIVING_COMPLETE = True
            walk_channel.stop()
            ding_channel.play(ding_sound)

        CURSOR_RECT.center = pygame.mouse.get_pos()
        SCREEN.blit(images.CURSOR, CURSOR_RECT)

        if pygame.sprite.spritecollide(player, watcher_group, False):
            error_channel.play(error_sound)
            walk_channel.stop()
            current_scene = "thanksgiving_failure"

        pygame.display.update()
        FPS_CLOCK.tick(constants.FPS)

def loadChristmasScene():
    global current_scene, CHRISTMAS_COMPLETE
    player = SpriteFactory.createSprite("Player", constants.WIDTH // 2, constants.HEIGHT - 50, movement_speed=6)

    snowman = SpriteFactory.createSprite("Object", constants.WIDTH // 2, 25, image_path="media/snowman.png")
    snowman.rect.x -= snowman.rect.width // 2

    snowball = SpriteFactory.createSprite("Snowball", constants.WIDTH // 2, (constants.HEIGHT // 4) * 3, x_speed=-4, y_speed=-4)
    bar = SpriteFactory.createSprite("Object", 0, 0, image_path="media/bar.png")

    snow_background = pygame.image.load("media/snow_background.png")

    collision_group = pygame.sprite.Group()

    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                block = SpriteFactory.createSprite("Object", j * 105, i * 15, image_path="media/ice block.png")
                collision_group.add(block)
    
    collision_group.add(bar)

    while current_scene == "christmas":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if snowball.rect.bottom >= constants.HEIGHT - 10:
            pygame.mixer.Sound("media/error.mp3").play()
            current_scene = "christmas_failure"
            break

        if pygame.sprite.collide_rect(snowball, snowman):
            pygame.mixer.Sound("media/ding.mp3").play()
            current_scene = "christmas_aftermath"
            CHRISTMAS_COMPLETE = True
            break

        player.update_left_right()
        snowball.update(collision_group, bar)

        bar.rect.center = player.rect.center
        bar.rect.y -= 20

        SCREEN.fill(colors.BLACK)

        SCREEN.blit(snow_background, (0, 0))

        for block in collision_group:
            SCREEN.blit(block.image, block.rect)
        
        SCREEN.blit(player.image, player.rect)

        SCREEN.blit(bar.image, bar.rect)
        SCREEN.blit(snowman.image, snowman.rect)
        SCREEN.blit(snowball.image, snowball.rect)

        CURSOR_RECT.center = pygame.mouse.get_pos()
        SCREEN.blit(images.CURSOR, CURSOR_RECT)

        pygame.display.update()
        FPS_CLOCK.tick(constants.FPS)

def loadSecretScene():
    global current_scene
    player = SpriteFactory.createSprite("Player", constants.WIDTH // 2, constants.HEIGHT // 2, movement_speed=3)

    collision_group = pygame.sprite.Group()

    

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text