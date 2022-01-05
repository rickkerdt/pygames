#--- Space Invaders by Rick Paassen ---#

#--- initialize ---#
import pygame
import os
import time
import random

from pygame import color
pygame.font.init()

#--- Fonts ---#
MAIN_FONT = pygame.font.SysFont("comicsans", 40)

#--- Display settings ---#
FPS = 60
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")  # Window display name

#--- Settings ---#
LEVEL_NUM = 0
LIVES_NUM = 5
ENEMY_NUM = []
WAVE_NUM = 5
ENEMY_SHIP_HEALTH = 100
PLAYER_SHIP_HEALTH = 100

VEL = 5
ENEMY_VEL = 5

#--- Colors --#
WHITE = 255, 255, 255
RED = 255, 0, 0

#--- Load assets ---#
RED_SPACE_SHIP = pygame.image.load(os.path.join(
    'Space Invaders', 'Assets', 'pixel_ship_red_small.png'))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join(
    'Space Invaders', 'Assets', 'pixel_ship_green_small.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join(
    'Space Invaders', 'Assets', 'pixel_ship_blue_small.png'))

YELLOW_SPACE_SHIP = pygame.image.load(os.path.join(
    'Space Invaders', 'Assets', 'pixel_ship_yellow.png'))  # Player ship

RED_LASER = pygame.image.load(os.path.join(
    'Space Invaders', 'Assets', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join(
    'Space Invaders', 'Assets', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join(
    'Space Invaders', 'Assets', 'pixel_laser_blue.png'))
YELLOW_LASER = pygame.image.load(os.path.join(
    'Space Invaders', 'Assets', 'pixel_laser_yellow.png'))

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join(
    'Space Invaders', 'Assets', 'background-black.png')), (WIDTH, HEIGHT))

#--- Classes ---#


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.lasers_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


#--- Main loop ---#


def main():
    run = True
    clock = pygame.time.Clock()

    player = Player(300, 650)
    enemies = ENEMY_NUM
    enemy_vel = ENEMY_VEL
    level = LEVEL_NUM
    wave_length = WAVE_NUM

    def redraw_window():  # Drawing content on the screen
        WIN.blit(BACKGROUND, (0, 0))
        lives_label = MAIN_FONT.render(f"Lives: {LIVES_NUM}", 1, (WHITE))
        level_label = MAIN_FONT.render(f"Level: {LEVEL_NUM}", 1, (WHITE))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            lives = 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(
                    50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - VEL > 0:  # left
            player.x -= VEL
        if keys[pygame.K_RIGHT] and player.x + VEL + player.get_width() < WIDTH:  # right
            player.x += VEL
        if keys[pygame.K_UP] and player.y - VEL > 0:  # up
            player.y -= VEL
        if keys[pygame.K_DOWN] and player.y + VEL + player.get_height() + 15 < HEIGHT:  # down
            player.y += VEL

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        redraw_window()


main()
