"""
Jonathan Crescenzo, 10/30/2023
    This is a testing program to try out using pygame, and by with that many
modules in general. Likely this will be a sidescrolling game since the
tutorial I originally used was a top down space invaders clone.

scrolling bg: https://github.com/russs123/pygame_tutorials/blob/main/Infinite_Background/scroll_tut.py
"""
import pygame  # game creation import
import random  # for enemy placement
import math  # for collision and other stuff
import time  # for bg scrolling
from pygame import mixer  # for handling music / sounds

# Initialize
pygame.init()

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Display
screen_width = 1500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Caption and Icon
pygame.display.set_caption("The Mountain of Asareth")
icon = pygame.image.load('mountain.png')  # comment b/c no image yet
pygame.display.set_icon(icon)

# Background Image
bg = pygame.image.load("bg.png")
bg_width = bg.get_width()
bg_rect = bg.get_rect()

# Defining Game Variables
scroll = 0
tiles = math.ceil(screen_width / bg_width) + 1

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 0  # 0 = left border
playerY = 280  # 0 = upper border
playerX_change = 0
playerY_change = 0

# Enemies
enemyImg = []  # making lists so we can store multiple enemies
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3  # number of enemies we want
for i in range(num_of_enemies):  # want to be able to loop through them
    enemyImg.append(pygame.image.load('enemy1.png'))  # .append because its a list now, was '=' originally
    enemyX.append(random.randint(1200, 1436))
    enemyY.append(random.randint(0, 600))
    enemyX_change.append(2)  # for moving enemy left and right, etc
    # enemyY_change.append(40)  # for y axis enemy movment, set to 40 so we can move it down in the loop later

# Bullet (player)
bulletImg = pygame.image.load('bullet.png')
bulletX = 20
bulletY = 280
bulletX_change = 30
bulletY_change = 0
bullet_state = "ready"  # ready: You cant see the bullet on the screen


# Functions
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):  # function for shooting the bullet out of the player
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 10, y + 16))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:  # trial and testing untill finding propper distance between enemy and bullet to call it a collision
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))

    # Draw Scrolling Background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))
        bg_rect.x = i * bg_width + scroll
        pygame.draw.rect(screen, (255, 0, 0), bg_rect, 1)
    # Scroll Background
    scroll -= 4

    # Reset Scroll
    if abs(scroll) > bg_width:
        scroll = 0

    # Event Handler
    for event in pygame.event.get():  # for every event in all of the events happening in the game window
        # Quit
        if event.type == pygame.QUIT:
            running = False

        # Key Bindings
        if event.type == pygame.KEYDOWN:  # checks if the key is being pressed down, KEYUP would check if its up / releasing
            #print("Keystroke Pressed")
            if event.key == pygame.K_UP:
                playerY_change = -6
            if event.key == pygame.K_DOWN:
                playerY_change = 6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_SPACE:  # checks spacebar press
                if bullet_state == "ready":  # makes sure bullet doesnt teleport to us by requiring the ready state
                    # bullet_sound = mixer.Sound(mixer.Sound('laser.wav'))  # loads bullet sound when firing
                    # bullet_sound.play()  # plays the bullet sound
                    bulletX = playerX  # to counter bullet following player x coord
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)  # calling fire bullet funct when space is pressed
                    # originally playerX but that gets the bullet stuck on our current x location

        if event.type == pygame.KEYUP:
            #print("Keystroke Released")
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                    or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0


    # Enemy Movement
    for i in range(num_of_enemies):
        rSpeedNum = random.randint(-5, -1)
        enemyX_change[i] = rSpeedNum
        enemyX[i] += enemyX_change[i]  # continuous movement
        enemy(enemyX[i], enemyY[i], i)

        # Enemy collision with left edge of screen
        if enemyX[i] <= 0:
            enemyX[i] = random.randint(1360, 1435)
            enemyY[i] = random.randint(0, 536)

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX,
                                bulletY)
        if collision:
            #explosion_sound = mixer.Sound(
            #    mixer.Sound('explosion.wav'))  # loads explosion sound on collision with enemy
            #explosion_sound.play()  # plays that sound
            bulletX = playerX  # reset bullet to its starting point
            bullet_state = "ready"  # change the state since the bullet isn't shown anymore
            #score_value += 1  # increase score by 1 each time we hit, score_value change for scoring system
            # now we need to get the enemy to respawn upon being hit, up to the enemy block to take stuff!
            enemyX[i] = random.randint(1436, 1500)
            enemyY[i] = random.randint(0, 536)  # now the enemy will respawn as it should
        #enemy(enemyX[i], enemyY[i], i)  # moved to multi enemy for loop, needed i's and also to specify enemy image

    # Bullet Movement
    if bulletX >= screen_width:  # handles when bullet goes off screen (only x axis rn)
        bulletX = 280
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletX += bulletX_change

    # Keyboard Input Application for Player
    playerX += playerX_change
    playerY += playerY_change

    # Left and Right Wall Border Control for Player
    """
    playerX = min(max(playerX, 0), screen_width)
    playerY = min(max(playerY, 0), screen_height)
    """
    playerX = min(max(playerX, 0), screen_width - 63)
    playerY = min(max(playerY, 0), screen_height - 63)
    """
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1436:
        playerX = 1436
    elif playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536
    """

    print('X: {}      Y: {}'.format(playerX,playerY))

    player(playerX, playerY)

    # Update
    pygame.display.update()

pygame.quit()
