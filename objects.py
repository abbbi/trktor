#!/usr/bin/pyton3
"""
Simons jump game
"""
from dataclasses import dataclass


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
    vehicle: object = None


@dataclass
class vehicle:
    asset: str
    height: int
    width: int
    sound: str
    y: int = 0
    x: int = 200
    x_start: int = 200
