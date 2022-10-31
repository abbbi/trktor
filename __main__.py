#!/usr/bin/pyton3
"""
Simons jump game
"""
import sys
import os
import copy
import math
from datetime import datetime
from glob import glob
import json
import random
import pygame
import pygame_menu
from pygame import mixer

from objects import obstacle, spawnedobstacle, world, surface, game, vehicle


def load_obstacles(path):
    obstacles = []
    for odir in glob(f"{path}/*/"):
        with open(f"{odir}/info.json", "r") as j:
            info = json.loads(j.read())
        this = obstacle(
            asset=f"{odir}/img.png",
            width=info["width"],
            height=info["height"],
            x=info["x"],
            image=pygame.image.load(f"{odir}/img.png").convert_alpha(),
        )
        try:
            this.powerup = info["powerup"]
        except KeyError:
            pass
        obstacles.append(this)

    return obstacles


def load_worlds(path):
    worlds = []
    for odir in sorted(glob(f"{path}/*/"), key=len):
        with open(f"{odir}/info.json", "r") as j:
            info = json.loads(j.read())
        this = world(asset=f"{odir}/img.png", y=info["y"], name=info["name"])
        worlds.append(this)

    return worlds


def load_vehicles(path):
    vehicles = []
    for odir in sorted(glob(f"{path}/*/"), key=len):
        with open(f"{odir}/info.json", "r") as j:
            info = json.loads(j.read())
        this = vehicle(
            asset=f"{odir}/img.png",
            sound=f"{odir}/sound.mp3",
            width=info["width"],
            height=info["height"],
            x=info["x"],
            name=info["name"],
            image=pygame.image.load(f"{odir}/img.png"),
        )
        vehicles.append(this)

    return vehicles


def menu(screen, gameobj):
    mixer.music.load(f"{gameobj.media}/menu.mp3")
    mixer.music.play()

    worlds = load_worlds(game.media_worlds)
    vehicles = load_vehicles(game.media_vehicles)

    # defaults
    gameobj.world = worlds[random.randrange(0, len(worlds))]
    gameobj.vehicle = vehicles[random.randrange(0, len(vehicles))]

    myimage = pygame_menu.baseimage.BaseImage(image_path=f"{gameobj.media}/menu.png")
    mytheme = pygame_menu.themes.THEME_ORANGE.copy()
    mytheme.title_background_color = (0, 0, 0)
    mytheme.background_color = myimage

    mymenu = pygame_menu.Menu(
        height=gameobj.screen_h, theme=mytheme, title="Trktor", width=gameobj.screen_w
    )

    def set_difficulty(one, two):
        gameobj.scrollstep += two
        gameobj.jump_height -= 3

    def set_tractor(one, two):
        if two is not None:
            gameobj.vehicle = vehicles[two]

    def set_world(one, two):
        if two is not None:
            gameobj.world = worlds[two]
            gameobj.platform_height = gameobj.world.y

    gameobj.username = mymenu.add.text_input("Name: ", default="Simon", maxchar=10)
    mymenu.add.selector(
        "Modus: ", [("Einfach", 0), ("Schwer", 10)], onchange=set_difficulty
    )

    vhlist = []
    vhlist.append(("Egal", None))
    for idx, x in enumerate(vehicles):
        vhlist.append((x.name, idx))
    mymenu.add.selector("Traktor:", vhlist, onchange=set_tractor)
    wlist = []
    wlist.append(("Egal", None))
    for idx, x in enumerate(worlds):
        wlist.append((x.name, idx))
    mymenu.add.selector("Welt", wlist, onchange=set_world)

    mymenu.add.button("Spiel Starten", mymenu.disable)
    mymenu.add.button("Quit", pygame_menu.events.EXIT)
    mymenu.mainloop(screen)


def getsf(item):
    return pygame.transform.scale(item.image, (item.height, item.width))


def draw_coins(screen, gameobj, vh_jumping):
    coinsf = getsf(vh_jumping)
    s = vh_jumping.width
    for _ in range(0, gameobj.coins):
        coin_rect = coinsf.get_rect(center=(s, 45))
        screen.blit(coinsf, coin_rect)
        s += vh_jumping.width + 20


def spawn_obstacle(gameobj, obstacles):
    obstacle_ = obstacles[random.randrange(0, len(obstacles))]
    obstaclesf = getsf(obstacle_)

    obstacle_rect = obstaclesf.get_rect(center=(obstacle_.x, gameobj.platform_height))

    if obstacle_.powerup is not None:
        obstacle_rect.y = random.randrange(200, 300)
    else:
        obstacle_rect.y = gameobj.platform_height - 30
        gameobj.score += 1
    obstacle_rect.x = obstacle_.x
    obstacle_.hit = False

    return spawnedobstacle(
        obstacle=obstacle_,
        sf=obstaclesf,
        rect=obstacle_rect,
        velocity=gameobj.y_velocity,
    )


def handle_collide(gameobj, vehicle_rect, spawned):
    if vehicle_rect.colliderect(spawned.rect) and spawned.obstacle.powerup is None:
        if gameobj.coins == 0:
            return True
        if spawned.obstacle.hit is False:
            gameobj.hit_sound.play()
            gameobj.coins -= 1
            gameobj.score -= 1
            spawned.obstacle.hit = True

    if vehicle_rect.colliderect(spawned.rect) and spawned.obstacle.powerup == "coin":
        if gameobj.coins < gameobj.maxcoins and spawned.obstacle.hit is False:
            gameobj.coins += 1
            gameobj.coin_sound.play()
            spawned.obstacle.hit = True
            # move coin to position 3 so it appears the vehicle
            # has "consumed" it.
            spawned.rect.x = 3

    return False


def rotate(image, angle):
    loc = image.get_rect().center
    rot = pygame.transform.rotate(image, angle)
    rot.get_rect().center = loc
    return rot


def mainloop(gameobj, clock, screen):
    gameobj.coin_sound = mixer.Sound(f"{gameobj.media}/coin.ogg")
    gameobj.hit_sound = mixer.Sound(f"{gameobj.media}/hit.ogg")
    background = draw_background(screen, gameobj.world.asset)
    obstacles = load_obstacles(game.media_obstacles)
    background_width = background.get_width()
    gameobj.tiles = math.ceil(game.screen_w / background_width) + 1

    ##
    # draw vehicle, play sound
    ##
    thisvehicle = gameobj.vehicle
    thisvehicle.y = gameobj.platform_height
    vh_standing = thisvehicle
    vh_jumping = copy.copy(thisvehicle)
    vh_jumping.height = 66
    vh_jumping.width = 44
    vhsf_standing = getsf(vh_standing)
    vhsf_jumping = getsf(vh_jumping)
    vehicle_rect = vhsf_standing.get_rect(center=(thisvehicle.x_start, thisvehicle.y))
    mixer.music.load(thisvehicle.sound)
    mixer.music.play(loops=-1)

    ##
    # spawn first obstacle
    ##
    spawned = spawn_obstacle(gameobj, obstacles)
    jump = mixer.Sound(f"{gameobj.media}/jump.ogg")
    font = pygame.font.Font(f"{gameobj.media}/freesansbold.ttf", 24)

    angle = 0
    while True:
        pygame.event.get()
        if handle_collide(gameobj, vehicle_rect, spawned) is True:
            break

        if angle >= 360:
            angle = 0

        updated = []
        if spawned.rect.x <= 5:
            spawned = spawn_obstacle(gameobj, obstacles)
            scored = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            gameobj.jumps = True
            jump.play()
        if keys_pressed[pygame.K_ESCAPE]:
            sys.exit(1)

        for i in range(0, gameobj.tiles):
            updated.append(
                screen.blit(background, (i * background_width + gameobj.scroll, 0))
            )

        spawned.rect.x -= 3
        gameobj.scroll -= gameobj.scrollstep

        if abs(gameobj.scroll) > background_width:
            gameobj.scroll = 0

        if spawned.obstacle.hit is True and spawned.obstacle.powerup is None:
            if scored is True:
                gameobj.score -= 1
                scored = False
            if angle >= 360:
                angle = 0
            angle += 1
            spawned.rect.y -= spawned.velocity
            spawned.velocity -= gameobj.y_gravity
            updated.append(screen.blit(rotate(spawned.sf, angle), spawned.rect))
        else:
            updated.append(screen.blit(spawned.sf, spawned.rect))

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
            updated.append(screen.blit(vhsf_jumping, vehicle_rect))
        else:
            vehicle_rect = vhsf_jumping.get_rect(
                center=(thisvehicle.x_start, gameobj.platform_height)
            )
            updated.append(screen.blit(vhsf_standing, vehicle_rect))

        draw_coins(screen, gameobj, vh_jumping)

        img = font.render(f"FPS: [{int(clock.get_fps())}]", True, (0, 0, 0))
        updated.append(screen.blit(img, (690, 10)))

        pygame.display.update(updated)
        updated = []
        clock.tick(gameobj.fps)

    mixer.music.stop()
    crash = mixer.Sound(f"{gameobj.media}/crash.ogg")
    crash.play()


def draw_background(screen, asset):
    background = pygame.image.load(asset).convert()
    screen.blit(background, (0, 0))
    return background


def main():
    mixer.pre_init()
    pygame.init()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((game.screen_w, game.screen_h))
    screen.set_alpha(None)
    pygame.display.set_caption(game.caption)

    start_time = datetime.now()
    while True:
        gameobj = game()
        menu(screen, gameobj)
        print(gameobj.username.get_value())
        gameobj.platform_height = gameobj.world.y
        mainloop(gameobj, clock, screen)
        print(gameobj.score)


if __name__ == "__main__":
    main()
