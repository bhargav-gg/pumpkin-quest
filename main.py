import pygame

import sys
import os
import time

import images
import colors
import story
import constants

import SceneSetter

#Initialize game via singleton
SceneSetter.initialize()

#Top-level game loop
#Handles switching between scenes/levels
while True:
    SceneSetter.SCREEN.fill(colors.BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #Scene switching
    if SceneSetter.current_scene == "credits":
        SceneSetter.loadCreditScene()
    elif SceneSetter.current_scene == "story":
        SceneSetter.loadStoryScene(story.intro_story, "menu")
    elif SceneSetter.current_scene == "menu":
        SceneSetter.loadMenuScene()
    elif SceneSetter.current_scene == "halloween_story":
        SceneSetter.loadStoryScene(story.halloween_story, "halloween")
    elif SceneSetter.current_scene == "thanksgiving_story":
        SceneSetter.loadStoryScene(story.thanksgiving_story, "thanksgiving")
    elif SceneSetter.current_scene == "christmas_story":
        SceneSetter.loadStoryScene(story.christmas_story, "christmas")
    elif SceneSetter.current_scene == "secret_story":
        SceneSetter.loadStoryScene(story.secret_story, "secret")
    elif SceneSetter.current_scene == "halloween":
        SceneSetter.loadHalloweenScene()
    elif SceneSetter.current_scene == "thanksgiving":
        SceneSetter.loadThanksgivingScene()
    elif SceneSetter.current_scene == "christmas":
        SceneSetter.loadChristmasScene()
    elif SceneSetter.current_scene == "secret":
        SceneSetter.loadSecretScene()
    elif SceneSetter.current_scene == "thanksgiving_failure":
        SceneSetter.loadStoryScene(story.thanksgiving_failure, "thanksgiving")
    elif SceneSetter.current_scene == "christmas_failure":
        SceneSetter.loadStoryScene(story.christmas_failure, "christmas")
    elif SceneSetter.current_scene == "secret_failure":
        SceneSetter.loadStoryScene(story.secret_failure, "secret")
    elif SceneSetter.current_scene == "halloween_aftermath":
        SceneSetter.loadStoryScene(story.halloween_aftermath, "menu")
    elif SceneSetter.current_scene == "thanksgiving_aftermath":
        SceneSetter.loadStoryScene(story.thanksgiving_aftermath, "menu")
    elif SceneSetter.current_scene == "christmas_aftermath":
        SceneSetter.loadStoryScene(story.christmas_aftermath, "menu")
    elif SceneSetter.current_scene == "secret_aftermath":
        SceneSetter.loadStoryScene(story.secret_aftermath, None)
        pygame.quit()
        sys.exit()
    
    #Draw custom cursor
    SceneSetter.CURSOR_RECT.center = pygame.mouse.get_pos()
    SceneSetter.SCREEN.blit(images.CURSOR, SceneSetter.CURSOR_RECT)

    #Tick
    pygame.display.update()
    SceneSetter.FPS_CLOCK.tick(constants.FPS)