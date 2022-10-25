#!/usr/bin/pyton3
"""
Simons jump game
"""
import sys
import math
from dataclasses import dataclass
import pygame


@dataclass
class obstacle:
    asset: str
    height: int
    width: int
    y: int = 660
    x: int = 600


@dataclass
class surface:
    asset: str
    height: int
    width: int
    y: int
    x: int


@dataclass
class obstacles:
    obstacle: list


@dataclass
class game:
    screen_w: int = 800
    screen_h: int = 800
    fps: int = 60
    jump_height: int = 25
    y_gravity: float = 0.6
    y_velocity = jump_height
    scroll: int = 0
    caption: str = "simons traktor spiel"
    tiles: int = 0
    jumps: bool = False


@dataclass
class vehicle:
    asset: str
    height: int
    width: int
    y: int = 660
    x: int = 200
    y_start: int = 660
    x_start: int = 200


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((game.screen_w, game.screen_h))
    pygame.display.set_caption(game.caption)

    vh_standing = vehicle(asset="assets/trktor_standing.png", height=99, width=64)
    vh_jumping = vehicle(
        asset="assets/trktor_jumping.png",
        height=77,
        width=64,
    )

    vhsf_standing = pygame.transform.scale(
        pygame.image.load(
            vh_standing.asset,
        ),
        (vh_standing.height, vh_standing.width),
    )

    vhsf_jumping = pygame.transform.scale(
        pygame.image.load(
            vh_jumping.asset,
        ),
        (vh_jumping.height, vh_jumping.width),
    )
    obstacle_ = obstacle(asset="assets/rock.png", width=77, height=64)
    obstaclesf = pygame.transform.scale(
        pygame.image.load(obstacle_.asset), (obstacle_.width, obstacle_.height)
    )
    background = pygame.image.load("assets/background.png")
    background_width = background.get_width()

    gameobj = game()
    gameobj.tiles = math.ceil(game.screen_w / background_width) + 1

    vehicle_rect = vhsf_standing.get_rect(center=(vehicle.x, vehicle.y))
    obstacle_rect = obstaclesf.get_rect(center=(obstacle.x, obstacle.y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()

        if vehicle_rect.colliderect(obstacle_rect):
            print("YOU MESSED UP")
            break

        if keys_pressed[pygame.K_SPACE]:
            gameobj.jumps = True

        for i in range(0, gameobj.tiles):
            screen.blit(background, (i * background_width + gameobj.scroll, 0))

        obstacle_rect.x -= 3
        if obstacle_rect.x < 0:
            obstacle_rect.x = obstacle.x

        screen.blit(obstaclesf, obstacle_rect)
        gameobj.scroll -= 5

        if abs(gameobj.scroll) > background_width:
            gameobj.scroll = 0

        if gameobj.jumps:
            vehicle.y -= gameobj.y_velocity
            gameobj.y_velocity -= gameobj.y_gravity
            if gameobj.y_velocity < -gameobj.jump_height:
                gameobj.jumps = False
                gameobj.y_velocity = gameobj.jump_height

            vehicle_rect = vhsf_jumping.get_rect(
                center=(
                    vehicle.x,
                    vehicle.y,
                )
            )
            screen.blit(vhsf_jumping, vehicle_rect)
        else:
            vehicle_rect = vhsf_jumping.get_rect(
                center=(vehicle.x_start, vehicle.y_start)
            )
            screen.blit(vhsf_standing, vehicle_rect)

        pygame.display.update()
        clock.tick(gameobj.fps)


if __name__ == "__main__":
    main()

""""
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
"""
