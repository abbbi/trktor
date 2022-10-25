#!/usr/bin/pyton3
"""
Simons jump game
"""
import sys
import math
from datetime import datetime
from dataclasses import dataclass
from glob import glob
import json
import random
import pygame
import pygame_menu
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
    jump_height: int = 22
    y_gravity: float = 0.6
    y_velocity = jump_height
    scroll: int = 0
    scrollstep: int = 5
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
    text_render = font.render(text, 1, (255, 255, 255))
    x, y, w, h = text_render.get_rect()
    x, y = position
    return screen.blit(text_render, (x, y))


def menu(screen, gameobj, clock, background, text="Start"):
    mixer.music.load(f"{gameobj.media}/menu.mp3")
    mixer.music.play()

    b2 = button(screen, (gameobj.screen_h / 2, gameobj.screen_w / 2), text)
    cont = False
    while cont is False:
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b2.collidepoint(pygame.mouse.get_pos()):
                    cont = True
                    break
        if keys_pressed[pygame.K_s]:
            cont=True
            break

        pygame.display.update()


def mainloop(gameobj, clock, background, screen):
    mixer.music.load(f"{gameobj.media}/trktor.mp3")
    mixer.music.play()

    vh_standing = vehicle(asset="assets/trktor_standing.png", height=99, width=64)
    vhsf_standing = pygame.transform.scale(
        pygame.image.load(
            vh_standing.asset,
        ),
        (vh_standing.height, vh_standing.width),
    )
    vh_jumping = vehicle(
        asset="assets/trktor_jumping.png",
        height=77,
        width=64,
    )
    vhsf_jumping = pygame.transform.scale(
        pygame.image.load(
            vh_jumping.asset,
        ),
        (vh_jumping.height, vh_jumping.width),
    )

    coin = vehicle(
        asset="assets/trktor_jumping.png",
        height=56,
        width=36,
    )
    coinsf = pygame.transform.scale(
        pygame.image.load(
            vh_jumping.asset,
        ),
        (coin.height, coin.width),
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
        if obstacle_rect.x <= 5:
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
        gameobj.scroll -= gameobj.scrollstep

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

        s = coin.width
        for c in range(0, gameobj.coins):
            coin_rect = coinsf.get_rect(center=(s, 45))
            screen.blit(coinsf, coin_rect)
            s += coin.width + 20
        pygame.display.update()
        clock.tick(gameobj.fps)

    mixer.music.stop()
    crash = mixer.Sound(f"{gameobj.media}/crash.ogg")
    crash.play()


def main():
    pygame.init()
    mixer.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((game.screen_w, game.screen_h))
    pygame.display.set_caption(game.caption)

    gameobj = game()
    background = pygame.image.load("assets/background.png")
    screen.blit(background, (0, 0))
    text = "Start"

    start_time = datetime.now()
    while True:
        menu(screen, gameobj, clock, background, text=text)
        mainloop(gameobj, clock, background, screen)
        text = "Neustart"
        gameobj.coins -= 1

        crash_time = datetime.now()
        since_crash = crash_time - start_time

        if since_crash.seconds >= 30:
            start_time = datetime.now()
            print("Raising level")
            gameobj.fps += 20
            gameobj.scrollstep += 5

        if gameobj.coins == 0:
            break

    menu(screen, gameobj, clock, background, text="Gameover")


if __name__ == "__main__":
    main()
