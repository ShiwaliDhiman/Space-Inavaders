import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("resources/Space.jpg")

# background sound
mixer.music.load("resources/background.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("resources/ufo (1).png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("resources/space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = [pygame.image.load("resources/alien.png"),
            pygame.image.load("resources/alien.png"),
            pygame.image.load("resources/enemy.png"),
            pygame.image.load("resources/enemy.png"),
            pygame.image.load("resources/alien.png"),
            pygame.image.load("resources/enemy.png"),
            pygame.image.load("resources/alien.png")
            ]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 7

for i in range(number_of_enemies):
    # enemyImg.append(pygame.image.load("resources/alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# bullet
# ready - you can't see the bullet on the screen
# fire - the bullet is currently moving
bulletImg = pygame.image.load("resources/bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 0.95
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font("resources/Cosmic Blaster.ttf", 80)

# enter text
enter_font = pygame.font.Font("resources/Garland.ttf", 60)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    enter_text = enter_font.render("Press Enter To Play Again", True, (255, 255, 255))
    screen.blit(over_text, (150, 100))
    screen.blit(score, (300, 300))
    screen.blit(enter_text, (100, 430))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyY - bulletY), 2) + math.pow((enemyX - bulletX), 2))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            elif event.key == pygame.K_SPACE:
                if enemyY[5] >= 2000:
                    break
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("resources/laser.wav")
                    bullet_sound.play()
                    # get the x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_RETURN and enemyY[5] >= 2000:
                mixer.music.load("resources/background.wav")
                mixer.music.play(-1)
                score_value = 0
                for i in range(number_of_enemies):
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # RGB = Red,Green,Blue
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))

    playerX += playerX_change
    # checking for boundaries of spaceship so it does not go out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(number_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            # game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("resources/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    if enemyY[5] >= 2000:
        screen.fill((0, 0, 0))
        game_over_text()
        pygame.mixer.music.stop()
    pygame.display.update()
