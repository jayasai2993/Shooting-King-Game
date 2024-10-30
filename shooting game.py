import pygame
import random
import math

pygame.init()

# creating game window
screen = pygame.display.set_mode((800, 600))

# title and icon
title = " shooting king"
icon = pygame.image.load('target.png')
pygame.display.set_caption(title)
pygame.display.set_icon(icon)
# background
bg = pygame.image.load('Space-Free-PNG-Image.png')

pygame.mixer.music.load('WhatsApp Audio 2024-08-01 at 20.23.11_bba1dfa5.mp3')
pygame.mixer.music.play(-1)
bullet_sound = pygame.mixer.Sound('GUNSHOT.wav')
explosion_sound = pygame.mixer.Sound('explosion3.wav')

# player
player_img = pygame.image.load('jet-pack.png')
playerx = 368
playery = 516
playerx_change = 0

# enemy
num_of_enemies = 6
enemy_img = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('monster.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(20, 120))
    enemyx_change.append(0.6)
    enemyy_change.append(40)

# Bullet
bullet_img = pygame.image.load('bullet.png')
bulletx = 0
bullety = 516
bullety_change = -4
bullet_state = "ready"

score = 0

score_font = pygame.font.Font('Koulen-Regular.ttf', 32)
scorex = 10
scorey = 10

game_over_font = pygame.font.Font('Koulen-Regular.ttf', 64)
game_overx = 280
game_overy = 200

restart_font = pygame.font.Font('Koulen-Regular.ttf', 32)
restartx = 220
restarty = 300

game_status = "running"


def show_game_over(x, y):
    global game_status
    game_over_img = game_over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(game_over_img, (x, y))
    pygame.mixer.music.stop()
    game_status = "end"


def show_restart(x, y):
    restart_img = restart_font.render(" To Restart the Game press R ", True, (0, 255, 0))
    screen.blit(restart_img, (x, y))


def show_score(x, y):
    score_img = score_font.render("score " + str(score), True, (255, 255, 255))
    screen.blit(score_img, (x, y))


def iscollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance < 25:
        return True
    else:
        return False


def bullet(x, y):
    screen.blit(bullet_img, (x + 16, y + 10))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


game_on = True
while game_on:
    # background RGB
    screen.fill((45, 51, 71))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -1.3
            if event.key == pygame.K_RIGHT:
                playerx_change = 1.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_state = "fire"
                    bulletx = playerx
                    bullet(bulletx, bullety)
                    bullet_sound.play()
            if event.key == pygame.K_r:
                if game_status == "end":
                    game_status = "running"
                    score = 0
                    playerx = 368
                    pygame.mixer.music.play(-1)
                    for i in range(num_of_enemies):
                        enemyx[i] = random.randint(0, 736)
                        enemyy[i] = random.randint(20, 120)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # bullet movements
    if bullet_state == "fire":
        if bullety < 10:
            bullety = 516
            bullet_state = "ready"
        bullety += bullety_change
        bullet(bulletx, bullety)

    # enemy
    for i in range(num_of_enemies):
        # game over

        if enemyy[i] > 466:
            show_restart(restartx, restarty)
            show_game_over(game_overx, game_overy)
            for j in range(num_of_enemies):
                enemyy[j] = 1200

        # .
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx[i] = 0
            enemyx_change[i] = 0.6
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx[i] = 736
            enemyx_change[i] = -0.6
            enemyy[i] += enemyy_change[i]
        enemy(enemyx[i], enemyy[i], i)

        # collisions
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullety = 516
            bullet_state = "ready"
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(20, 120)
            score += 1
            explosion_sound.play()
    show_score(scorex, scorey)

    # player
    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    player(playerx, playery)

    pygame.display.update()
