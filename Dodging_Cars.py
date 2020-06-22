#import modules

from random import random
import pygame
from pygame import mixer_music
import random
import time
import math

# Initializing pygame and game window size and game name
pygame.init()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Car Dodge')
clock = pygame.time.Clock()

## Setting game elements
# Background road
backgroundImg = pygame.image.load('road.png')
# Car
carImg = pygame.image.load('car.png')
# Obstacles
obsImg = pygame.image.load('obstacles.png')

## Sound effects
# Game sound
background_music = pygame.mixer.Sound('driving_sound.wav')
# Crash sound
crash_effect = pygame.mixer.Sound('outbound_crash.wav')

# Create car object
def car(x,y):
    gameDisplay.blit(carImg, (x,y))

# Create obstacles object
def obstacles(obs_x, obs_y):
    gameDisplay.blit(obsImg, (obs_x, obs_y))

# Start Message
def start_msg():
    font = pygame.font.SysFont("freesansbold", 25)
    text = font.render("Use Left / Right Arrow Keys to dodge. Game begins in 5 secs.", True, (0, 0, 0))
    gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
    pygame.display.flip()

# Create Crash Message
def crash_msg(milsec):
    font = pygame.font.SysFont("freesansbold", 40)
    text = font.render("Crashed! Press 'Esc' to reset, 'q' to exit", True, (255, 255, 255))
    gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(milsec)

def game_loop():
    # Initialize variables for use in while loop
    x_move = 0
    kill = 1  # Quits on pressing q, after crash
    start = 1 # Flag to indicate first loop iteration
    crashed = False

    # Initialize co-ordinates for cars
    x = (display_width * 0.475)
    y = (display_height * 0.83) + 2

    # Initialize co-ordinates for obstacles
    obs_y = random.sample(range(0, display_height), 4)
    obs_x = random.sample(range(0, display_width), 4)
    # When the game starts, the car and obstacle should not spawn at the same x location.
    while x in obs_x:
        obs_x = random.sample(range(0, display_width), 4)

    # Loop begins
    while not crashed:
        # Adding background image
        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(backgroundImg, (0, 0))

        # If it's the first iteration if while loop
        if start == 1:
            start_msg()
            car(x,y)
            pygame.display.update()
            time.sleep(3)
            background_music.play(-1)
            start = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = -20
                elif event.key == pygame.K_RIGHT:
                    x_move = 20
                if event.key == pygame.K_ESCAPE:
                    x_move = 0
                    x = display_width * 0.475
                    kill = 1
                    crash_effect.stop()
                if event.key == pygame.K_q and kill == 0:
                    quit()
            if event.type == pygame.KEYUP:
                x_move = 0

        # If the Car crashes into the screen-boundary
        if x > (display_width - 20) or x < -20:
            background_music.stop()
            crash_effect.play(1)
            kill = 0
            x_move = 0
            crash_msg(100)

        # Continue music again
        background_music.play(-1)

        # Check if crash between Car and obstacles occurs
        obs_crash_check = []
        for i in range(4):
            obs_crash_check.append((x <= obs_x[i] <= (x + 45) or obs_x[i] <= x <= obs_x[i] + 45) and \
                        (obs_y[i] <= y <= obs_y[i] + 95 or y <= obs_y[i] <= y + 95) or \
                        (x <= obs_x[i] <= (x + 45) or obs_x[i] <= x <= obs_x[i] + 45) and \
                        (obs_y[i] <= y <= obs_y[i] + 95 or y <= obs_y[i] <= y + 95)
                              )
        # If Car and obstacles crashes
        if sum(obs_crash_check) >= 1:
            kill = 0
            x_move = 0
            crash_msg(0)
        else:
            x += x_move
            for i in range(4):
                obstacles(obs_x[i], obs_y[i])
                obs_y[i] += 20
                car(x, y)
                if obs_y[i] > display_height:
                    obs_x[i] = random.randrange(0, display_width)
                    obs_y[i] = 0

        pygame.display.update()
        clock.tick(40)

# Call the Game Loop
game_loop()

pygame.quit()
