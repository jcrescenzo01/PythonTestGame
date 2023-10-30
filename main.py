"""
Jonathan Crescenzo, 10/30/2023
    This is a testing program to try out using pygame, and by with that many
modules in general. Likely this will be a sidescrolling game since the
tutorial I originally used was a top down space invaders clone.
"""
import pygame  # game creation import
import random  # for enemy placement
import math  # for collision and other stuff
from pygame import mixer  # for handling music / sounds

# Initialize
pygame.init()

# Display
screen = pygame.display.set_mode((800, 600))

# Caption and Icon
pygame.display.set_caption("This is a Test")
#icon = pygame.image.load('ufo.png')    # comment b/c no image yet
#pygame.display.set_icon(icon)

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    pygame.display.update()

    for event in pygame.event.get():    # for every event in all of the events happening in the game window
        if event.type == pygame.QUIT:   # these 2 lines allow quit
            running = False