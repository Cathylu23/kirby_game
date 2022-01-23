import pygame
import os
import random
import math
pygame.init()
pygame.font.init()
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

#window 
HEIGHT = 800
WIDTH = 600
SIZE = (HEIGHT, WIDTH)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Aircraft War")
# icon = pygame.image.load("space.png")
# pygame.display.set.icon(icon)
clock = pygame.time.Clock()
FPS = 60

# # background
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, 'background.png'))
background = pygame.transform.scale(background, (800, 600))

# score-----------------------------------------------------------------
score = 0
font1 = pygame.font.Font('freesansbold.ttf', 40)

def show_score():
    text = f"score: {score}"
    score_render = font1.render(text, True, (255, 255, 255))
    screen.blit(score_render, (10, 10))


# player---------------------------------------------------------------
player = pygame.image.load(os.path.join(current_path, 'player.png'))
player = pygame.transform.scale(player, (150, 150))
player_x = 300
player_y = 400
player_stepX = 0 #speed of player


# enemy----------------------------------------------------------------
number_of_enemies = 8
class Enemy():
    def __init__(self):
        self.enemy = pygame.image.load(os.path.join(current_path, 'energy.png'))
        self.enemy = pygame.transform.scale(self.enemy, (100, 100))
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 250)
        self.step = random.randint(2, 6)
    # reset the postion of bullet
    def reset(self):
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 200)

enemies = []
for i in range(number_of_enemies):
    enemies.append(Enemy())

def distance(bx, by, ex, ey):
    a = bx - ex
    b = by - ey
    return math.sqrt(a*a + b*b) #square root

def show_enemy():
    global is_over
    for e in enemies:
        screen.blit(e.enemy, (e.x, e.y))
        e.x += e.step
        if(e.x > 700 or e.x < 0):
            e.step *= -1
            e.y += 40 #speed
            if e.y > 400:
                is_over = True
                print("Game over")
                enemies.clear()

is_over = False
font = pygame.font.Font('freesansbold.ttf', 50)
def check():
    if is_over:
        lost_text = "You lost"
        over_text = "Game over"
        render1 = font.render(over_text, True, (0, 0, 255))
        render2 = font.render(lost_text, True, (0, 0, 255))
        screen.blit(render1, (300, 200))
        screen.blit(render2, (350, 100))


# bullet--------------------------------------------------------------------------
class Bullet():
    def __init__(self):
        self.bullet = pygame.image.load(os.path.join(current_path, 'bullet.png'))
        self.bullet = pygame.transform.scale(self.bullet, (50, 50))
        self.x = player_x + 50
        self.y = player_y + 15
        self.step = 10 #moving speed of bullet
    # hit
    def hit(self):
        global score
        for e in enemies:
            if (distance(self.x, self.y, e.x, e.y) < 10):
                bullets.remove(self)
                e.reset()
                score += 1

bullets = [] #save current bullets

# show bullets
def show_bullets():
    for b in bullets:
        screen.blit(b.bullet, (b.x, b.y))
        b.hit()
        b.y -= b.step 
        if b.y < 0:
            bullets.remove(b)

# main loop
running = True
while running:
    screen.blit(background, (0, 0))
    show_score()
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
              running = False
         if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_RIGHT:
                 player_stepX = 8
             elif event.key == pygame.K_LEFT:
                player_stepX = -8
             elif event.key == pygame.K_SPACE :
                # create a bullet
                b = Bullet()
                bullets.append(Bullet())

         if event.type == pygame.KEYUP:
            player_stepX = 0
    
    screen.blit(player, (player_x, player_y))
    player_x += player_stepX
    
    # range of player
    if player_x > 650:
        player_x = 650
    elif player_x < 0:
        player_x = 0
  
    show_enemy()
    show_bullets()
    check()
    pygame.display.update()
    clock.tick(FPS)

# how to import music in pygame 
