import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys

camera = cv2.VideoCapture(0)
pygame.init()

display_width = 1000
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
bg_col = (238, 238, 238)

button_blue = (23, 37, 86)
button_blue_hover = (7, 18, 58)

high_score = 0

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ASL Buddy')
clock = pygame.time.Clock()

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, i, a, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        tagText = pygame.font.Font('freesansbold.ttf', 18)

        startButton = pygame.Rect(0, 0, w, h)
        startButton.center = (x, y)

        if x+(w/2) > mouse[0] > x-(w/2) and y+(h/2) > mouse[1] > y-(h/2):
            pygame.draw.rect(gameDisplay, a, startButton)
            if click[0] == 1 and action != None:
                if action == "start":
                    game_loop()
        else:
            pygame.draw.rect(gameDisplay, i, startButton)

        ButtonSurf, ButtonRect = text_objects(msg, tagText, white)
        ButtonRect.center = (x, y)
        gameDisplay.blit(ButtonSurf, ButtonRect)

def game_loop():
    gameExit = False

    titleText = pygame.font.Font('freesansbold.ttf', 115)
    TitleSurf, TitleRect = text_objects("Game Screen", titleText, black)
    TitleRect.center = ((display_width/2), (display_height/4))

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        ret, frame = camera.read()
		
        gameDisplay.fill([0,0,0])
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        gameDisplay.blit(frame, (0,0))

        pygame.display.update()
        clock.tick(60)

def game_intro():  
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        gameDisplay.fill(bg_col)

        titleText = pygame.font.Font('freesansbold.ttf', 115)
        TitleSurf, TitleRect = text_objects("ASL Buddy", titleText, black)
        TitleRect.center = ((display_width/2), (display_height/4))

        tagText = pygame.font.Font('freesansbold.ttf', 18)
        TagSurf, TagRect = text_objects("Learn the ASL alphabet while trying to beat your high score!", tagText, black)
        TagRect.center = ((display_width/2), (display_height/2.9))

        scoreText = pygame.font.Font('freesansbold.ttf', 30)
        ScoreSurf, ScoreRect = text_objects("High Score: " + str(high_score), scoreText, black)
        ScoreRect.center = ((display_width/2), (display_height/2))

        button("Start Game!", display_width/2, 375, 150, 50, button_blue, button_blue_hover, "start")

        gameDisplay.blit(TitleSurf, TitleRect)
        gameDisplay.blit(TagSurf, TagRect)
        gameDisplay.blit(ScoreSurf, ScoreRect)
        
        pygame.display.update()
        clock.tick(15)

game_intro()
game_loop()
pygame.quit()
quit()