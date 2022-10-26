#!/usr/bin/pyton3
"""
Simons jump game
"""
import sys
import copy
import math
from datetime import datetime
from glob import glob
import json
import random
import pygame
import pygame_menu
from pygame import mixer

from objects import obstacle, world, surface, game, vehicle


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
            sound=f"{odir}/sound.mp3",
            width=info["width"],
            height=info["height"],
            x=info["x"],
        )
        vehicles.append(this)

    return vehicles


def menu(screen, gameobj, clock, background):
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

    def set_difficulty(one, two):
        gameobj.scrollstep += two
        gameobj.jump_height -= 3

    def set_tractor(one, two):
        gameobj.vehicle = two

    menu.add.selector(
        "Modus: ", [("Einfach", 0), ("Schwer", 10)], onchange=set_difficulty
    )
    menu.add.selector(
        "Traktor:", [("Egal", None), ("Gruen", 0), ("Rot", 1)], onchange=set_tractor
    )
    menu.add.button("Spiel Starten", menu.disable)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    menu.mainloop(screen)


def draw_coins(screen, gameobj, vh_jumping):
    coinsf = pygame.transform.scale(
        pygame.image.load(
            vh_jumping.asset,
        ),
        (vh_jumping.height, vh_jumping.width),
    )

    s = vh_jumping.width
    for c in range(0, gameobj.coins):
        coin_rect = coinsf.get_rect(center=(s, 45))
        screen.blit(coinsf, coin_rect)
        s += vh_jumping.width + 20


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
    gameobj.coin_sound = mixer.Sound(f"{gameobj.media}/coin.ogg")
    gameobj.hit_sound = mixer.Sound(f"{gameobj.media}/hit.ogg")

    obstacles = load_obstacles(game.media_obstacles)
    vehicles = load_vehicles(game.media_vehicles)

    thisvehicle = vehicles[random.randrange(0, len(vehicles))]
    if gameobj.vehicle is not None:
        thisvehicle = vehicles[gameobj.vehicle]
    thisvehicle.y = gameobj.platform_height

    mixer.music.load(thisvehicle.sound)
    mixer.music.play()

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

    start_time = datetime.now()
    while True:
        gameobj = game()
        gameobj.platform_height = world.y
        menu(screen, gameobj, clock, background)
        mainloop(gameobj, clock, background, screen)


if __name__ == "__main__":
    main()