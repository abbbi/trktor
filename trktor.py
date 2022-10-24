#!/usr/bin/pyton3
"""
 Jump game example with scrolling background
"""
import sys
import math
import pygame

pygame.init()
SCREEN_W = 800
SCREEN_H = 800

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Jumping in PyGame")

X_POSITION, Y_POSITION = 400, 660

O_X_POSITION = X_POSITION
O_Y_POSITION = Y_POSITION

jumping = False

Y_GRAVITY = 0.6
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT

STANDING_SURFACE = pygame.transform.scale(
    pygame.image.load("assets/trktor_standing.png"), (99, 64)
)
JUMPING_SURFACE = pygame.transform.scale(
    pygame.image.load("assets/trktor_jumping.png"), (77, 64)
)
BACKGROUND = pygame.image.load("assets/background.png")
BACKGROUND_W = BACKGROUND.get_width()
scroll = 0

tiles = math.ceil(SCREEN_W / BACKGROUND_W) + 1

mario_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_SPACE]:
        jumping = True

    for i in range(0, tiles):
        SCREEN.blit(BACKGROUND, (i * BACKGROUND_W + scroll, 0))

    scroll -= 5

    if abs(scroll) > BACKGROUND_W:
        scroll = 0

    if jumping:
        Y_POSITION -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT

        mario_rect = JUMPING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(JUMPING_SURFACE, mario_rect)
    else:
        mario_rect = STANDING_SURFACE.get_rect(center=(O_X_POSITION, O_Y_POSITION))
        SCREEN.blit(STANDING_SURFACE, mario_rect)

    pygame.display.update()
    CLOCK.tick(60)
