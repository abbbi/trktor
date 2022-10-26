#!/usr/bin/pyton3
"""
Simons jump game
"""
import sys
import copy
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
    powerup: str = None
    hit: bool = False


@dataclass
class world:
    asset: str
    y: int = 0


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
    screen_h: int = 600
    fps: int = 60
    jump_height: int = 19
    y_gravity: float = 0.6
    y_velocity = jump_height
    scroll: int = 0
    scrollstep: int = 5
    caption: str = "simons traktor spiel"
    tiles: int = 0
    jumps: bool = False
    media = "assets/"
    media_obstacles = f"{media}/obstacles/"
    media_vehicles = f"{media}/vehicles/"
    media_worlds = f"{media}/worlds/"
    coins: int = 3
    maxcoins: int = coins
    hit_sound: object = None
    coin_sound: object = None
    platform_height: int = 0


@dataclass
class vehicle:
    asset: str
    height: int
    width: int
    y: int = 0
    x: int = 200
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
        try:
            this.powerup = info["powerup"]
        except KeyError:
            pass
        obstacles.append(this)

    return obstacles


def load_worlds(path):
    worlds = []
    for odir in glob(f"{path}/*/"):
        print(f"{odir}/info.json")
        with open(f"{odir}/info.json", "r") as j:
            info = json.loads(j.read())
        this = world(
            asset=f"{odir}/img.png",
            y=info["y"],
        )
        worlds.append(this)

    return worlds


def load_vehicles(path):
    vehicles = []
    for odir in glob(f"{path}/*/"):
        print(f"{odir}/info.json")
        with open(f"{odir}/info.json", "r") as j:
            info = json.loads(j.read())
        this = vehicle(
            asset=f"{odir}/img.png",
            width=info["width"],
            height=info["height"],
            x=info["x"],
        )
        vehicles.append(this)

    return vehicles


def button(screen, position, text):
    font = pygame.font.SysFont("Arial", 50)
    text_render = font.render(text, 1, (255, 255, 255))
    x, y, w, h = text_render.get_rect()
    x, y = position
    return screen.blit(text_render, (x, y))


def menu(screen, gameobj, clock, background, text="Start"):
    mixer.music.load(f"{gameobj.media}/menu.mp3")
    mixer.music.play()
    myimage = pygame_menu.baseimage.BaseImage(
        image_path="assets/worlds/0/img.png",
    )
    mytheme = pygame_menu.themes.THEME_ORANGE.copy()
    mytheme.title_background_color = (0, 0, 0)
    mytheme.background_color = myimage

    menu = pygame_menu.Menu(
        height=gameobj.screen_h, theme=mytheme, title="Trktor", width=gameobj.screen_w
    )

    menu.add.button("Play", menu.disable)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    menu.mainloop(screen)


def draw_coins(screen, gameobj, vh_jumping):
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

    s = coin.width
    for c in range(0, gameobj.coins):
        coin_rect = coinsf.get_rect(center=(s, 45))
        screen.blit(coinsf, coin_rect)
        s += coin.width + 20


def spawn_obstacle(gameobj, obstaclesf, obstacle_rect, obstacles):
    obstacle_ = obstacles[random.randrange(0, len(obstacles))]
    obstaclesf = pygame.transform.scale(
        pygame.image.load(obstacle_.asset), (obstacle_.width, obstacle_.height)
    )
    if obstacle_.powerup is not None:
        obstacle_rect.y = random.randrange(200, 300)
    else:
        obstacle_rect.y = gameobj.platform_height - 20
    obstacle_rect.x = obstacle_.x
    obstacle_.hit = False
    return obstacle_, obstaclesf


def handle_collide(gameobj, vehicle_rect, obstacle_rect, obstacle_):
    if vehicle_rect.colliderect(obstacle_rect) and obstacle_.powerup is None:
        if gameobj.coins == 0:
            return True
        if obstacle_.hit is False:
            gameobj.hit_sound.play()
            gameobj.coins -= 1
            obstacle_.hit = True

    if vehicle_rect.colliderect(obstacle_rect) and obstacle_.powerup == "coin":
        if gameobj.coins < gameobj.maxcoins and obstacle_.hit is False:
            gameobj.coins += 1
            gameobj.coin_sound.play()
            obstacle_.hit = True

    return False


def mainloop(gameobj, clock, background, screen):
    mixer.music.load(f"{gameobj.media}/trktor.mp3")
    mixer.music.play()
    gameobj.coin_sound = mixer.Sound(f"{gameobj.media}/coin.ogg")
    gameobj.hit_sound = mixer.Sound(f"{gameobj.media}/hit.ogg")

    obstacles = load_obstacles(game.media_obstacles)
    vehicles = load_vehicles(game.media_vehicles)

    thisvehicle = vehicles[random.randrange(0, len(vehicles))]
    thisvehicle.y = gameobj.platform_height

    vh_standing = thisvehicle
    vh_jumping = copy.copy(thisvehicle)
    vh_jumping.height = 66
    vh_jumping.width = 44

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

    obstacle_ = obstacles[random.randrange(0, len(obstacles))]
    obstaclesf = pygame.transform.scale(
        pygame.image.load(obstacle_.asset), (obstacle_.width, obstacle_.height)
    )
    background_width = background.get_width()
    gameobj.tiles = math.ceil(game.screen_w / background_width) + 1
    vehicle_rect = vhsf_standing.get_rect(center=(thisvehicle.x_start, thisvehicle.y))

    obstacle_rect = obstaclesf.get_rect(center=(obstacle_.x, gameobj.platform_height))
    obstacle_rect.y = gameobj.platform_height - 20
    obstacle_rect.x = obstacle_.x

    while True:
        if obstacle_rect.x <= 5:
            (obstacle_, obstaclesf) = spawn_obstacle(
                gameobj, obstaclesf, obstacle_rect, obstacles
            )

        if handle_collide(gameobj, vehicle_rect, obstacle_rect, obstacle_) is True:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()
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
            thisvehicle.y -= gameobj.y_velocity
            gameobj.y_velocity -= gameobj.y_gravity
            if gameobj.y_velocity < -gameobj.jump_height:
                gameobj.jumps = False
                gameobj.y_velocity = gameobj.jump_height

            vehicle_rect = vhsf_jumping.get_rect(
                center=(
                    thisvehicle.x_start,
                    thisvehicle.y,
                )
            )
            screen.blit(vhsf_jumping, vehicle_rect)
        else:
            vehicle_rect = vhsf_jumping.get_rect(
                center=(thisvehicle.x_start, gameobj.platform_height)
            )
            screen.blit(vhsf_standing, vehicle_rect)

        draw_coins(screen, gameobj, vh_jumping)
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

    worlds = load_worlds(game.media_worlds)
    world = worlds[random.randrange(0, len(worlds))]
    background = pygame.image.load(world.asset)
    screen.blit(background, (0, 0))
    text = "Start"

    start_time = datetime.now()
    while True:
        gameobj = game()
        gameobj.platform_height = world.y
        menu(screen, gameobj, clock, background, text=text)
        mainloop(gameobj, clock, background, screen)
        text = "Neustart"


if __name__ == "__main__":
    main()
