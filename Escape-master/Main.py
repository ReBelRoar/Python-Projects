import pygame
import random
import math

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
# Background
background = pygame.image.load('background.jpg')
# Title and Logo
pygame.display.set_caption('Escape')
logo = pygame.image.load("ufo.png")
pygame.display.set_icon(logo)
# Player
player = pygame.image.load('player.png')
pos1 = 378
pos2 = 530
pos_change = 0
# Enemy
enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
na_of_enemies = 6
no_of_bullets = 0
for i in range(na_of_enemies):
    enemy.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.8)
    enemyY_change.append(35)
# Bullet
# Ready- you can'y see the bullet on the screen
# Fire- the bullet is currently moving
bullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 530
bulletX_change = 0
bulletY_change = 5
bullet_state = 'ready'


# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 30)
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 60)


def show_score(x, y):
    scor = font.render('Score :' + str(score), True, (255, 255, 255))
    screen.blit(scor, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (240, 260))


# draw image on screen

def player_info(x, y):
    screen.blit(player, (x, y))


# draw enemy image on screen

def enemy_info(x, y, i):
    screen.blit(enemy[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet, (x + 16, y + 10))
    global no_of_bullets
    no_of_bullets += 1


def Collision(enemyX, enemyY, bulletX, bulletY):
    dis = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if dis < 25:
        return True
    else:
        return False


# For Hold the Game Screen and exit only when quit event is performed
con = True
while con:
    screen.fill((40, 40, 40))
    # Fill the background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            con = False
        # Changing position on the basis of key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pos_change = 4
            if event.key == pygame.K_LEFT:
                pos_change = -4
            if event.key == pygame.K_SPACE:
                # Here if bullet is not on screen only when another bullet is fired
                if bullet_state == 'ready':
                    # position of bullet is changing according to the player pos
                    bulletX = pos1
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pos_change = 0

    pos1 += pos_change
    # Boundary of player so it does't go outside of screen
    if pos1 <= 0:
        pos1 = 0
    elif pos1 >= 736:
        pos1 = 736
    # Enemy movement
    for i in range(na_of_enemies):
        # Game over
        if enemyY[i] > 300:
            for j in range(na_of_enemies):
                enemyY[i] = 1000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # Boundary of enemy so it does't go outside of screen
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.8
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.8
            enemyY[i] += enemyY_change[i]

        # collision
        collision = Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy_info(enemyX[i], enemyY[i], i)

    # ready- we can't see the movement of bullet
    # fire- we can see the bullet movement
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player_info(pos1, pos2)
    show_score(textX, textY)
    # For updating display
    pygame.display.update()
