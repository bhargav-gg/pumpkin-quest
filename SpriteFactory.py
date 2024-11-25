import pygame

from Object import Object
from Snowball import Snowball
from Watcher import Watcher
from Player import Player
from Letter import Letter

class SpriteFactory:
    @staticmethod
    def createSprite(name: str, x: int, y: int, x_speed: int = 0, movement_speed: int = 0, y_speed: int = 0, direction: str = "left", threshold: int = 0, image_path: str = "", letter: str = "") -> pygame.sprite.Sprite:
        if name == "Snowball":
            return Snowball(x, y, x_speed, y_speed)
        elif name == "Watcher":
            return Watcher(x, y, direction, threshold)
        elif name == "Player":
            return Player(x, y, movement_speed)
        elif name == "Object":
            return Object(x, y, image_path)
        elif name == "Letter":
            return Letter(x, y, letter, movement_speed)
        else:
            raise ValueError("Invalid sprite name")