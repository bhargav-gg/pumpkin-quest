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

#Contains position of centered logo
CENTERED_LOGO_POS = []

#pygame clock, screen, cursor rect
FPS_CLOCK = None
SCREEN = None
CURSOR_RECT = None

#Flags to mark compeltion of scenes
HALLOWEEN_COMPLETE = False
THANKSGIVING_COMPLETE = False
CHRISTMAS_COMPLETE = False

#Current scene, initialized to credits
current_scene = "credits"

def initialize():
    #Access global variables
    global CENTERED_LOGO_POS, FPS_CLOCK, SCREEN, CURSOR_RECT

    #Initialize pygame and hide default cursor
    pygame.init()
    pygame.mouse.set_visible(False)

    #If on Windows, set application ID for taskbar so application has a custom icon
    if os.name == 'nt':
        import ctypes
        myappid = u'Pumpkin Quest' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    #Set up logo positioning
    CENTERED_LOGO_POS = [(constants.WIDTH - images.LOGO.get_rect().size[0]) / 2, (constants.HEIGHT - images.LOGO.get_rect().size[1]) / 2]

    #FPS clock
    FPS_CLOCK = pygame.time.Clock()

    #Set up screen
    SCREEN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    SCREEN.fill(colors.BLACK)

    #Set up cursor
    CURSOR_RECT = images.CURSOR.get_rect()

    #Set up window title, icon
    pygame.display.set_caption("Pumpkin Quest")
    pygame.display.set_icon(images.LOGO_ICON)

def loadCreditScene():
    #Access global to change scene
    global current_scene

    #Wait for a second before showing logo
    time.sleep(1)

    #Render fade-in logo
    for i in range(255):
        SCREEN.fill(colors.BLACK)
        images.LOGO.set_alpha(i)
        SCREEN.blit(images.LOGO, CENTERED_LOGO_POS)
        pygame.display.update()
        time.sleep(0.005)
    
    #Keep logo up for a second
    time.sleep(1)

    #Render fade-out logo
    for i in range(255):
        SCREEN.fill(colors.BLACK)
        images.LOGO.set_alpha(255 - i)
        SCREEN.blit(images.LOGO, CENTERED_LOGO_POS)
        pygame.display.update()
        time.sleep(0.005)
    
    #Change scene to intro story
    current_scene = "story"

def loadStoryScene(strings, next_scene):
    #Access global to change scene
    global current_scene

    #Font for story text
    story_font = pygame.font.SysFont("Cascadia Code", constants.WIDTH // 20)

    #Click noise when player clicks through story
    click_sound = pygame.mixer.music("media/click.mp3")

    #Loop through each segment of the story, only proceeding to next segment when the player clicks
    for segment in strings:
        mouse_click = False

        #Loop while player hasn't clicked
        while not mouse_click:
            SCREEN.fill(colors.BLACK)

            drawText(SCREEN, segment, colors.RED, (constants.WIDTH // 10, constants.HEIGHT // 10, constants.WIDTH // 10 * 8, constants.HEIGHT // 10 * 8), story_font)

            CURSOR_RECT.center = pygame.mouse.get_pos()
            SCREEN.blit(images.CURSOR, CURSOR_RECT)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_click = True
                    pygame.mixer.music.play(click_sound)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

            FPS_CLOCK.tick(constants.FPS)
    
    #Change scene to next scene when all segments are done
    current_scene = next_scene

def loadMenuScene():
    #Access global to change scene accordingly
    global current_scene

    #Font for buttons, title
    font = pygame.font.SysFont("Cascadia Code", constants.WIDTH // 20)

    #Title
    title_font = pygame.font.SysFont("Cascadia Code", constants.WIDTH // 10)
    title = title_font.render("Pumpkin Quest", True, colors.RED)

    #Buttons
    halloween_button = Button.Button(colors.ORANGE, colors.BLACK, (constants.WIDTH // 2) - (constants.WIDTH // 8), (constants.HEIGHT // 16) * 7, constants.WIDTH // 4, constants.HEIGHT // 8, font, "Halloween")
    thanksgiving_button = Button.Button(colors.BROWN, colors.GOLD, (constants.WIDTH // 2) - (constants.WIDTH // 8), (constants.HEIGHT // 16) * 10, constants.WIDTH // 4, constants.HEIGHT // 8, font, "Thanksgiving")
    christmas_button = Button.Button(colors.CHRISTMAS_RED, colors.CHRISTMAS_GREEN, (constants.WIDTH // 2) - (constants.WIDTH // 8), (constants.HEIGHT // 16) * 13, constants.WIDTH // 4, constants.HEIGHT // 8, font, "Christmas")
    secret_button = Button.Button(colors.RED, colors.WHITE, (constants.WIDTH // 2) - (constants.WIDTH // 8), constants.HEIGHT // 2, constants.WIDTH // 4, constants.HEIGHT // 8, font, "???")

    #Click noise
    click_sound = pygame.mixer.music("media/click.mp3")

    #Button group list to determine which buttons to render
    button_group = [halloween_button]

    if HALLOWEEN_COMPLETE:
        button_group.append(thanksgiving_button)
    
    if THANKSGIVING_COMPLETE:
        button_group.append(christmas_button)
    
    if CHRISTMAS_COMPLETE:
        button_group = [secret_button]
    
    #Menu scene loop
    while current_scene == "menu":
        #pygame event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Detect click
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                #Detect if/which button was clicked and change scene accordingly
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
        
        #Render screen, buttons, title
        SCREEN.fill(colors.BLACK)

        for button in button_group:
            button.draw(SCREEN, colors.WHITE)
        
        SCREEN.blit(title, ((constants.WIDTH - title.get_width()) // 2, constants.HEIGHT // 16))
        
        CURSOR_RECT.center = pygame.mouse.get_pos()
        SCREEN.blit(images.CURSOR, CURSOR_RECT)

        #Tick
        pygame.display.update()
        FPS_CLOCK.tick(constants.FPS)

def loadHalloweenScene():
    #Global access to change scene, mark completion
    global current_scene, HALLOWEEN_COMPLETE

    #Player, pumpkin, darkness (fake lighting)
    player = SpriteFactory.createSprite("Player", 0, 300, movement_speed=2)
    pumpkin = SpriteFactory.createSprite("Object", 60, 210, image_path="media/halloween_pumpkin.png")
    darkness = SpriteFactory.createSprite("Object", 0, 0, image_path="media/darkness.png")

    #Footsteps, ding sound
    footstep_sound = pygame.mixer.music("media/footsteps.mp3")
    ding_sound = pygame.mixer.music("media/ding.mp3")

    #Text frame count for pumpkin acquired message (lasts for 180 frames/3 seconds)
    text_frame_count = 0

    #Font for text
    font = pygame.font.SysFont("Cascadia Code", constants.WIDTH // 20)

    #Hedges, dirt block groups
    hedges = pygame.sprite.Group()
    dirt = pygame.sprite.Group()

    #Channel for sound
    walk_channel = pygame.mixer.Channel(0)

    #Pumpkin acquired flag
    pumpkin_acquired = False

    #Map for easy placement of hedges/dirt blocks
    #0 = dirt
    #1 = hedge
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

    #Create sprites based on map
    for i in range(len(hedge_map)):
        for j in range(len(hedge_map[i])):
            if hedge_map[i][j] == 1:
                hedge = SpriteFactory.createSprite("Object", j * 50, i * 50, image_path="media/HEDGE.png")
                hedges.add(hedge)
            elif hedge_map[i][j] == 0:
                dirt_block = SpriteFactory.createSprite("Object", j * 50, i * 50, image_path="media/DIRT.png")
                dirt.add(dirt_block)
    
    #Main scene loop
    while current_scene == "halloween":
        #pygame event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #Get player's old position to detect end of movement
        old_rect = player.rect.copy()

        #Update player
        player.update(hedges)

        #Play footstep sound
        if not walk_channel.get_busy():
            walk_channel.play(footstep_sound)
        
        #But if player is not walking, immediately stop
        if old_rect == player.rect:
            walk_channel.stop()

        #Check for collision with pumpkin, mark as acquired
        if pygame.sprite.collide_rect(player, pumpkin):
            pumpkin_acquired = True
            ding_sound.play()

            pumpkin.rect.x = -100
            pumpkin.rect.y = -100
        
        #If player reaches right side of screen and pumpkin is acquired, player succeeds
        if player.rect.x >= constants.WIDTH - 25 and pumpkin_acquired:
            current_scene = "halloween_aftermath"
            HALLOWEEN_COMPLETE = True
            walk_channel.stop()
            ding_sound.play()
        
        #Render screen
        SCREEN.fill(colors.BLACK)

        for dirt_block in dirt:
            SCREEN.blit(dirt_block.image, dirt_block.rect)

        for hedge in hedges:
            SCREEN.blit(hedge.image, hedge.rect)
        
        #Render pumpkin if not acquired
        if not pumpkin_acquired:
            SCREEN.blit(pumpkin.image, pumpkin.rect)

        #Render player
        SCREEN.blit(player.image, player.rect)

        #Render darkness (fake lighting, follows player)
        darkness.rect.center = player.rect.center
        SCREEN.blit(darkness.image, darkness.rect)

        #Render text if pumpkin is acquired for 3 seconds/180 frames
        if pumpkin_acquired and text_frame_count < 180:
            text_frame_count += 1
            drawText(SCREEN, "You found the pumpkin!", colors.RED, (constants.WIDTH // 2, (constants.HEIGHT // 8) * 7, constants.WIDTH // 10 * 8, constants.HEIGHT // 10 * 8), font)
        
        #Render cursor
        CURSOR_RECT.center = pygame.mouse.get_pos()
        SCREEN.blit(images.CURSOR, CURSOR_RECT)

        #Tick
        pygame.display.update()
        FPS_CLOCK.tick(constants.FPS)

def loadThanksgivingScene():
    #Global access to change scene, mark completion
    global current_scene, THANKSGIVING_COMPLETE

    #Player
    player = SpriteFactory.createSprite("Player", 0, 300, movement_speed=2)

    #Background
    floorboards = pygame.image.load("media/floorboards.png")

    #Collision group to keep track of tables/chairs
    #Watcher group to keep track of watcher sprites
    collision_group = pygame.sprite.Group()
    watcher_group = pygame.sprite.Group()

    #Ding
    ding_channel = pygame.mixer.Channel(0)
    ding_sound = pygame.mixer.music("media/ding.mp3")

    #Error
    error_channel = pygame.mixer.Channel(1)
    error_sound = pygame.mixer.music("media/error.mp3")

    #Footsteps
    walk_channel = pygame.mixer.Channel(2)
    footstep_sound = pygame.mixer.music("media/wood_footsteps.mp3")

    #Pumpkin
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
        [0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 8, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 5, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 5, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 2, 0, 8, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 7, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 4, 0, 0],
        [0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0]
    ]

    #Create sprites based on grid
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
    
    #Main scene loop
    while current_scene == "thanksgiving":
        #pygame event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #Old player rect to detect end of movement
        old_rect = player.rect.copy()

        #Update player
        player.update(collision_group)

        #If player collides with pumpkin, mark as collected
        if pygame.sprite.collide_rect(player, pumpkin):
            pumpkin_collected = True
            ding_channel.play(ding_sound)
            pumpkin.rect.x = -100
            pumpkin.rect.y = -100
        
        #Play footstep sound
        if not walk_channel.get_busy():
            walk_channel.play(footstep_sound)
        
        #But if player is not walking, immediately stop
        if old_rect == player.rect:
            walk_channel.stop()
        
        #Render screen
        SCREEN.fill(colors.BLACK)
        SCREEN.blit(floorboards, (0, 0))

        #Update and render watchers
        for watcher in watcher_group:
            watcher.update()
            SCREEN.blit(watcher.image, watcher.rect)
        
        #Render tables/chairs
        for collision_object in collision_group:
            SCREEN.blit(collision_object.image, collision_object.rect)
    
        #Render pumpkin if not collected
        if not pumpkin_collected:
            SCREEN.blit(pumpkin.image, pumpkin.rect)
        
        #Render player
        SCREEN.blit(player.image, player.rect)

        #If pumpkin is collected and player reaches left side of screen, player succeeds
        if pumpkin_collected and player.rect.x <= 10:
            current_scene = "thanksgiving_aftermath"
            THANKSGIVING_COMPLETE = True
            walk_channel.stop()
            ding_channel.play(ding_sound)
        
        #Render cursor
        CURSOR_RECT.center = pygame.mouse.get_pos()
        SCREEN.blit(images.CURSOR, CURSOR_RECT)

        #If player collides with watcher, fail player
        if pygame.sprite.spritecollide(player, watcher_group, False):
            error_channel.play(error_sound)
            walk_channel.stop()
            current_scene = "thanksgiving_failure"
        
        #Tick
        pygame.display.update()
        FPS_CLOCK.tick(constants.FPS)

def loadChristmasScene():
    #Access global to change scene, mark completion
    global current_scene, CHRISTMAS_COMPLETE

    #Player
    player = SpriteFactory.createSprite("Player", constants.WIDTH // 2, constants.HEIGHT - 50, movement_speed=6)

    #Snowman
    snowman = SpriteFactory.createSprite("Object", constants.WIDTH // 2, 25, image_path="media/snowman.png")
    snowman.rect.x -= snowman.rect.width // 2

    #Snowball
    snowball = SpriteFactory.createSprite("Snowball", constants.WIDTH // 2, (constants.HEIGHT // 4) * 3, x_speed=-4, y_speed=-4)

    #Player's bar
    bar = SpriteFactory.createSprite("Object", 0, 0, image_path="media/bar.png")

    #Background
    snow_background = pygame.image.load("media/snow_background.png")

    #Collision group (ice blocks)
    collision_group = pygame.sprite.Group()

    #Grid for ice block placement
    #Each cell represents a 100x15 rectangle of the top half of the 
    #0 = no ice block
    #1 = ice block
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

    #Create ice blocks based on grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                block = SpriteFactory.createSprite("Object", j * 105, i * 15, image_path="media/ice block.png")
                collision_group.add(block)
    
    #Add bar to collision (so snowball doesn't go through)
    collision_group.add(bar)

    #Main scene loop
    while current_scene == "christmas":
        #pygame event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #If snowball hits bottom of screen, player loses
        if snowball.rect.bottom >= constants.HEIGHT - 10:
            pygame.mixer.music("media/error.mp3").play()
            current_scene = "christmas_failure"
            break

        #If snowball hits snowman, player wins
        if pygame.sprite.collide_rect(snowball, snowman):
            pygame.mixer.music("media/ding.mp3").play()
            current_scene = "christmas_aftermath"
            CHRISTMAS_COMPLETE = True
            break

        #Update player, snowball
        player.update_left_right()
        snowball.update(collision_group, bar)

        #Update bar position based on player's
        bar.rect.center = player.rect.center
        bar.rect.y -= 20

        #Render background
        SCREEN.fill(colors.BLACK)
        SCREEN.blit(snow_background, (0, 0))

        #Render ice blocks
        for block in collision_group:
            SCREEN.blit(block.image, block.rect)
        
        #Render player, bar, snowman, snowball
        SCREEN.blit(player.image, player.rect)
        SCREEN.blit(bar.image, bar.rect)
        SCREEN.blit(snowman.image, snowman.rect)
        SCREEN.blit(snowball.image, snowball.rect)

        #Render cursor
        CURSOR_RECT.center = pygame.mouse.get_pos()
        SCREEN.blit(images.CURSOR, CURSOR_RECT)

        #Tick
        pygame.display.update()
        FPS_CLOCK.tick(constants.FPS)

def loadSecretScene():
    #Access global to change scene
    global current_scene

    #Player
    player = SpriteFactory.createSprite("Player", constants.WIDTH // 2, (constants.HEIGHT // 8) * 7, movement_speed=7)

    #Drachova
    drachova = SpriteFactory.createSprite("Object", constants.WIDTH // 2, (constants.HEIGHT // 8) * 3, image_path="media/DRACHOVA.png")
    drachova.rect.x -= drachova.rect.width // 2
    drachova.rect.y -= drachova.rect.height // 2

    #Background
    background = SpriteFactory.createSprite("Object", 0, 0, image_path="media/secret_background.png")

    #Create letter placeholders for user interface for user to know what they have collected
    letter_group = pygame.sprite.Group()

    letter_r_place = SpriteFactory.createSprite("Object", (constants.WIDTH // 2) - 120, 25, image_path="media/-.png")
    letter_r_place.rect.x -= letter_r_place.rect.width // 2
    letter_group.add(letter_r_place)

    letter_e_place = SpriteFactory.createSprite("Object", (constants.WIDTH // 2) - 80, 25, image_path="media/-.png")
    letter_e_place.rect.x -= letter_e_place.rect.width // 2
    letter_group.add(letter_e_place)

    letter_d_place = SpriteFactory.createSprite("Object", (constants.WIDTH // 2) - 40, 25, image_path="media/-.png")
    letter_d_place.rect.x -= letter_d_place.rect.width // 2
    letter_group.add(letter_d_place)

    letter_f_place = SpriteFactory.createSprite("Object", (constants.WIDTH // 2), 25, image_path="media/-.png")
    letter_f_place.rect.x -= letter_f_place.rect.width // 2
    letter_group.add(letter_f_place)

    letter_o_place = SpriteFactory.createSprite("Object", (constants.WIDTH // 2) + 40, 25, image_path="media/-.png")
    letter_o_place.rect.x -= letter_o_place.rect.width // 2
    letter_group.add(letter_o_place)

    letter_n_place = SpriteFactory.createSprite("Object", (constants.WIDTH // 2) + 80, 25, image_path="media/-.png")
    letter_n_place.rect.x -= letter_n_place.rect.width // 2
    letter_group.add(letter_n_place)

    letter_t_place = SpriteFactory.createSprite("Object", (constants.WIDTH // 2) + 120, 25, image_path="media/-.png")
    letter_t_place.rect.x -= letter_t_place.rect.width // 2
    letter_group.add(letter_t_place)

    #Letters that will spawn/fall
    letters = ["R", "E", "D", "F", "O", "N", "T"]

    #Counter for frames
    frame_count = 0

    #Table to keep track of what letters have been collected
    collected_table = {
        "R" : False,
        "E" : False,
        "D" : False,
        "F" : False,
        "O" : False,
        "N" : False,
        "T" : False
    }

    #Groups for falling letters and enemies
    falling_letters_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    enemy_group.add(drachova)

    #Main scene loop
    while current_scene == "secret":
        #pygame event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #Spawn falling letter every 3 seconds
        if frame_count % 180 == 0 and frame_count != 0:
            letter = random.choice(letters)
            letter_obj = SpriteFactory.createSprite("FallingObject", random.randint(0, constants.WIDTH - 50), 0, movement_speed=3, image_path=f"media/{letter}.png", letter=letter)
            letter_obj.rect.y -= letter_obj.rect.height
            falling_letters_group.add(letter_obj)
        
        #Spawn enemy every 8 frames (7.5 times a second)
        if frame_count % 8 == 0:
            enemy = SpriteFactory.createSprite("FallingObject", random.randint(0, constants.WIDTH - 50), 0, movement_speed=5, image_path="media/ZERO.png")
            enemy.rect.y -= enemy.rect.height
            enemy_group.add(enemy)
        
        #Spawn cat every 3 seconds
        if frame_count % 180 == 0 and frame_count != 0:
            enemy = SpriteFactory.createSprite("FallingObject", random.randint(0, constants.WIDTH - 50), 0, movement_speed=3, image_path="media/cat.png")
            enemy.rect.y -= enemy.rect.height
            enemy_group.add(enemy)
        
        #Spawn midterm every 10 seconds
        if frame_count % 600 == 0 and frame_count != 0:
            enemy = SpriteFactory.createSprite("FallingObject", random.randint(0, constants.WIDTH - 50), constants.HEIGHT // 8, movement_speed=2, image_path="media/MIDTERM1.png")
            enemy.rect.y -= enemy.rect.height
            enemy_group.add(enemy)
        
        #End scene if all letters are collected
        if all(collected_table.values()):
            current_scene = "secret_aftermath"
        
        #Update player
        player.update(pygame.sprite.Group())

        #Update screen
        SCREEN.fill(colors.BLACK)
        SCREEN.blit(background.image, background.rect)
        SCREEN.blit(player.image, player.rect)
        SCREEN.blit(drachova.image, drachova.rect)
        
        #Draw enemies and collected letters
        for enemy in enemy_group:
            enemy.update()
            SCREEN.blit(enemy.image, enemy.rect)
        
        for letter in falling_letters_group:
            letter.update()
            SCREEN.blit(letter.image, letter.rect)

        for letter in letter_group:
            SCREEN.blit(letter.image, letter.rect)
        
        #Check for collision with falling letter
        collision = pygame.sprite.spritecollide(player, falling_letters_group, False)

        #If collision, play sound and update collected table
        if collision:
            collected_table[collision[0].letter] = True
            pygame.mixer.music("media/ding.mp3").play()

            if collision[0].letter == "R":
                letter_r_place.image = pygame.image.load("media/R.png")
            elif collision[0].letter == "E":
                letter_e_place.image = pygame.image.load("media/E.png")
            elif collision[0].letter == "D":
                letter_d_place.image = pygame.image.load("media/D.png")
            elif collision[0].letter == "F":
                letter_f_place.image = pygame.image.load("media/F.png")
            elif collision[0].letter == "O":
                letter_o_place.image = pygame.image.load("media/O.png")
            elif collision[0].letter == "N":
                letter_n_place.image = pygame.image.load("media/N.png")
            elif collision[0].letter == "T":
                letter_t_place.image = pygame.image.load("media/T.png")
            
            collision[0].rect.x = constants.WIDTH + 100
            collision[0].kill()
        
        #Check for collision with enemy, if collision, play sound and fail player
        if pygame.sprite.spritecollide(player, enemy_group, False):
            pygame.mixer.music("media/error.mp3").play()
            current_scene = "secret_failure"
        
        #Draw cursor
        CURSOR_RECT.center = pygame.mouse.get_pos()
        SCREEN.blit(images.CURSOR, CURSOR_RECT)

        #Update frame count
        frame_count += 1

        #Tick
        pygame.display.update()
        FPS_CLOCK.tick(constants.FPS)


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
# source: https://www.pygame.org/wiki/TextWrap
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