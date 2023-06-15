import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

# Game defaults
FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
FONT = pygame.font.SysFont('Verdana', 20)
PADDING_SIZE = 30

# Screen
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
playing = True
background = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
background_x1 = 0
background_x2 = background.get_width()
background_move = 3

# Goose animation images
IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
image_index = 0

# Player object
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect().move(0, HEIGHT // 2 - player.get_width() // 2)
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_left = [-4, 0]
player_move_up = [0, -4]

# Enemies
def create_enemy():
    # Define object
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(
        WIDTH,
        random.randint(
            PADDING_SIZE,
            HEIGHT - enemy.get_height()
        ),
        *enemy.get_size()
    )
    enemy_move = [random.randint(-8, -4), 0] # Define speed
    return [enemy, enemy_rect, enemy_move]

# Enemy creation event
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []

# Score
score = 0

# Bonuses
def create_bonus():
    # Define object
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_width = bonus.get_width()
    bonus_rect = pygame.Rect(
        random.randint(
            bonus_width,
            WIDTH - bonus_width
        ),
        -bonus.get_height(),
        *bonus.get_size()
    )
    bonus_move = [0, random.randint(4, 8)] # Define speed
    return [bonus, bonus_rect, bonus_move]

# Bonus creation event
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)
bonuses = []

# Switch image (animation)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)
bonuses = []

while playing:
    FPS.tick(3000)

    for event in pygame.event.get():
        # Don't finish game unless exited
        if event.type == QUIT:
            playing = False

        # Enemy creation trigger
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        # Bonus creation trigger
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        # Animation. Picture switch trigger
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1

            # Reset index to first image
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
    
    # Set display background
    background_x1 -= background_move
    background_x2 -= background_move

    if background_x1 < -background.get_width():
        background_x1 = background.get_width()

    if background_x2 < -background.get_width():
        background_x2 = background.get_width()

    main_display.blit(background, (background_x1,0))
    main_display.blit(background, (background_x2,0))

    keys = pygame.key.get_pressed() # Player activity

    # Go Down
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    # Go Right
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    # Go Left
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    # Go Up
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    main_display.blit(player, player_rect) # Print player
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20)) # Display score

    # Enemies activity
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2]) # Move every enemy based on randomly generated speed
        main_display.blit(enemy[0], enemy[1]) # Display enemy on a new location

        if player_rect.colliderect(enemy[1]):
            playing = False # If player has touched this object, game is over

    # Bonuses activity
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2]) # Move every bonus based on randomly generated speed
        main_display.blit(bonus[0], bonus[1]) # Display bonus on a new location

        if player_rect.colliderect(bonus[1]):
            # If player has touched this object
            bonuses.pop(bonuses.index(bonus)) # Consume bonus
            score += 1 # Increment score

    pygame.display.flip() # Reload main screen

    # delete elements that are no longer on the screen
    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy)) # If enemy is no longer on the screen, delete it

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            # If bonus is no longer on the screen, delete it
            bonuses.pop(bonuses.index(bonus))