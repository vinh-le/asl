import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import string
import random
import tensorflow as tf

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

pygame.init()

display_width = 1000
display_height = 480

black = (0, 0, 0)
white = (255, 255, 255)
bg_col = (238, 238, 238)
button_blue = (23, 37, 86)
button_blue_hover = (7, 18, 58)
timer_red = (128, 21, 21)

intro = True
high_score = 0

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ASL Buddy')
clock = pygame.time.Clock()

label_lines = [line.rstrip() for line
                   in tf.io.gfile.GFile("logs/trained_labels.txt")]

with tf.io.gfile.GFile("logs/trained_graph.pb", 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

def predict(image_data):

    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})

    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

    max_score = 0.0
    res = ''
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        if score > max_score:
            max_score = score
            res = human_string
    return res, max_score

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
                    intro = False
                    game_loop()
        else:
            pygame.draw.rect(gameDisplay, i, startButton)

        ButtonSurf, ButtonRect = text_objects(msg, tagText, white)
        ButtonRect.center = (x, y)
        gameDisplay.blit(ButtonSurf, ButtonRect)

def game_loop():

    gameExit = False
    
    global current_score
    current_score = 0

    timer_font = pygame.font.Font('freesansbold.ttf', 12)
    timer_sec = 5
    timer_text = timer_font.render("00:05", True, timer_red)

    timer = pygame.USEREVENT + 1                                                
    pygame.time.set_timer(timer, 1000)

    rand_letter = random.choice(string.ascii_uppercase)

    letterText = pygame.font.Font('freesansbold.ttf', 200)
    LetterSurf, LetterRect = text_objects(rand_letter, letterText, black)
    LetterRect.center = (180, 240)

    i = 0

    curr = ""

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == timer:    # checks for timer event
                if timer_sec > 0:
                    if curr == rand_letter:
                        current_score+=10
                        pygame.time.set_timer(timer, 1000)
                        timer_sec = 5
                        timer_text = timer_font.render("00:05", True, timer_red)
                        rand_letter = random.choice(string.ascii_uppercase)

                        letterText = pygame.font.Font('freesansbold.ttf', 200)
                        LetterSurf, LetterRect = text_objects(rand_letter, letterText, black)
                        LetterRect.center = (180, 240)
                    else:
                        timer_sec -= 1
                        timer_text = timer_font.render("00:%02d" % timer_sec, True, timer_red)
                else:
                    gameExit = True
                    end_screen(rand_letter)

                    


        gameDisplay.fill(bg_col)

        gameDisplay.blit(timer_text, (180,450))
        gameDisplay.blit(LetterSurf, LetterRect)

        scoreText = pygame.font.Font('freesansbold.ttf', 25)
        ScoreSurf, ScoreRect = text_objects("High Score: " + str(high_score), scoreText, black)
        ScoreRect.center = (180, 18)
        gameDisplay.blit(ScoreSurf, ScoreRect)


        currentScoreText = pygame.font.Font('freesansbold.ttf', 25)
        CurrentScoreSurf, CurrentScoreRect = text_objects("Current Score: " + str(current_score), currentScoreText, black)
        CurrentScoreRect.center = (180, 52)
        gameDisplay.blit(CurrentScoreSurf, CurrentScoreRect)

        ret, frame = camera.read()
        if ret:
            frame = cv2.flip(frame, 1)
        x1, y1, x2, y2 = 100, 100, 300, 300

        if ret:
            if i == 10:
                i = 0
                img_cropped = frame[y1:y2, x1:x2]
                image_data = cv2.imencode('.jpg', img_cropped)[1].tostring()

                res_tmp, score = predict(image_data)

                curr = res_tmp.upper()
        
        i+=1
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        gameDisplay.blit(frame, (display_width-640,0))



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
        TagRect.center = ((display_width/2), (display_height/2.75))

        scoreText = pygame.font.Font('freesansbold.ttf', 30)
        ScoreSurf, ScoreRect = text_objects("High Score: " + str(high_score), scoreText, black)
        ScoreRect.center = ((display_width/2), (display_height/2))

        button("Start Game!", display_width/2, 375, 150, 50, button_blue, button_blue_hover, "start")

        gameDisplay.blit(TitleSurf, TitleRect)
        gameDisplay.blit(TagSurf, TagRect)
        gameDisplay.blit(ScoreSurf, ScoreRect)
        
        pygame.display.update()
        clock.tick(15)

def end_screen(rand_letter):
    global high_score
    high_score = max(current_score,high_score)
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game_intro()

        gameDisplay.fill(bg_col)
        button("Start Over!", display_width/2, display_height-35, 150, 50, button_blue, button_blue_hover, "start")
        currentScoreText = pygame.font.Font('freesansbold.ttf', 35)

        MessageSurf, MessageRect = text_objects("You missed '" + str(rand_letter) + "'", currentScoreText, black)
        MessageRect.center = (display_width/2, 50)
        gameDisplay.blit(MessageSurf, MessageRect)

        image = pygame.image.load("alphabet/" + str(rand_letter) + ".png")
        gameDisplay.blit(image, (display_width/2-90, 100)) 

        CurrentScoreSurf, CurrentScoreRect = text_objects("Score: " + str(current_score), currentScoreText, black)
        CurrentScoreRect.center = (display_width/2, display_height/2 + 110)
        gameDisplay.blit(CurrentScoreSurf, CurrentScoreRect)

        HighScoreSurf, HighScoreRect = text_objects("High Score: " + str(high_score), currentScoreText, black)
        HighScoreRect.center = (display_width/2, display_height/2 + 150)
        gameDisplay.blit(HighScoreSurf, HighScoreRect)
        
        pygame.display.update()
        clock.tick(15)

        

with tf.compat.v1.Session() as sess:
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    game_intro()
    game_loop()
    pygame.quit()
    quit()