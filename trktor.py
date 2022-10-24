#!/usr/bin/pyton3
"""
Simons jump game
"""
import sys
import math
import pygame

pygame.init()
SCREEN_W = 800
SCREEN_H = 800

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))

pygame.display.set_caption("simons traktor spiel")

X_POSITION, Y_POSITION = 200, 660

ROCK_X_POSITION, ROCK_Y_POSITION = 600, 660

O_X_POSITION = X_POSITION
O_Y_POSITION = Y_POSITION

JUMPS = False

Y_GRAVITY = 0.6
JUMP_HEIGHT = 23
Y_VELOCITY = JUMP_HEIGHT

STANDING_SURFACE = pygame.transform.scale(
    pygame.image.load("assets/trktor_standing.png"), (99, 64)
)
JUMPING_SURFACE = pygame.transform.scale(
    pygame.image.load("assets/trktor_jumping.png"), (77, 64)
)
ROCK_SURFACE = pygame.transform.scale(pygame.image.load("assets/rock.png"), (77, 64))

BACKGROUND = pygame.image.load("assets/background.png")
BACKGROUND_W = BACKGROUND.get_width()

SCROLL = 0

tiles = math.ceil(SCREEN_W / BACKGROUND_W) + 1

trktor_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))
rock_rect = ROCK_SURFACE.get_rect(center=(ROCK_X_POSITION, ROCK_Y_POSITION))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()

    if trktor_rect.colliderect(rock_rect):
        print("YOU MESSED UP")
        break

    if keys_pressed[pygame.K_SPACE]:
        JUMPS = True

    for i in range(0, tiles):
        SCREEN.blit(BACKGROUND, (i * BACKGROUND_W + SCROLL, 0))

    rock_rect.x -= 3
    if rock_rect.x < 0:
        rock_rect.x = ROCK_X_POSITION

    SCREEN.blit(ROCK_SURFACE, rock_rect)

    SCROLL -= 5

    if abs(SCROLL) > BACKGROUND_W:
        SCROLL = 0

    if JUMPS:
        Y_POSITION -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            JUMPS = False
            Y_VELOCITY = JUMP_HEIGHT

        trktor_rect = JUMPING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(JUMPING_SURFACE, trktor_rect)
    else:
        trktor_rect = STANDING_SURFACE.get_rect(center=(O_X_POSITION, O_Y_POSITION))
        SCREEN.blit(STANDING_SURFACE, trktor_rect)

    pygame.display.update()
    CLOCK.tick(60)
