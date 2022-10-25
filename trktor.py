#!/usr/bin/pyton3
"""
Simons jump game
"""
import sys
import math
from dataclasses import dataclass
from glob import glob
import json
import random
import pygame
from pygame import mixer


@dataclass
class obstacle:
    asset: str
    height: int
    width: int
    x: int
    y: int = 660


@dataclass
class surface:
    asset: str
    height: int
    width: int
    y: int
    x: int


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
    media = "assets/"
    media_obstacles = f"{media}/obstacles/"
    coins: int = 5


@dataclass
class vehicle:
    asset: str
    height: int
    width: int
    y: int = 660
    x: int = 200
    y_start: int = 660
    x_start: int = 200


def load_obstacles(path):
    obstacles = []
    for odir in glob(f"{path}/*/"):
        print(f"{odir}/info.json")
        with open(f"{odir}/info.json", "r") as j:
            info = json.loads(j.read())
        this = obstacle(
            asset=f"{odir}/img.png",
            width=info["width"],
            height=info["height"],
            x=info["x"],
        )
        obstacles.append(this)

    return obstacles


def button(screen, position, text):
    font = pygame.font.SysFont("Arial", 50)
    text_render = font.render(text, 1, (255, 0, 0))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h))
    return screen.blit(text_render, (x, y))


def menu(screen):
    b2 = button(screen, (400, 400), "Start")
    cont = False
    while cont is False:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b2.collidepoint(pygame.mouse.get_pos()):
                    cont = True
                    break
        pygame.display.update()


def main():
    pygame.init()
    mixer.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((game.screen_w, game.screen_h))
    pygame.display.set_caption(game.caption)

    gameobj = game()
    background = pygame.image.load("assets/background.png")
    screen.blit(background, (0, 0))
    menu(screen)

    mixer.music.load(f"{gameobj.media}/trktor.mp3")
    mixer.music.play()

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
    obstacles = load_obstacles(game.media_obstacles)
    obstacle_ = obstacles[random.randrange(0, len(obstacles))]
    obstaclesf = pygame.transform.scale(
        pygame.image.load(obstacle_.asset), (obstacle_.width, obstacle_.height)
    )

    background_width = background.get_width()

    gameobj.tiles = math.ceil(game.screen_w / background_width) + 1

    vehicle_rect = vhsf_standing.get_rect(center=(vehicle.x, vehicle.y))
    obstacle_rect = obstaclesf.get_rect(center=(obstacle_.x, obstacle.y))

    while True:
        if obstacle_rect.x < vehicle_rect.x:
            obstacle_ = obstacles[random.randrange(0, len(obstacles))]
            obstaclesf = pygame.transform.scale(
                pygame.image.load(obstacle_.asset), (obstacle_.width, obstacle_.height)
            )

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
            jump = mixer.Sound(f"{gameobj.media}/jump.ogg")
            jump.play()

        for i in range(0, gameobj.tiles):
            screen.blit(background, (i * background_width + gameobj.scroll, 0))

        obstacle_rect.x -= 3
        if obstacle_rect.x < 0:
            obstacle_rect.x = obstacle_.x

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
