import pygame

from Object import Object
from Snowball import Snowball
from Watcher import Watcher
from Player import Player
from FallingObject import FallingObject

# Factory class to create sprites
class SpriteFactory:
    # Create a sprite based on the name
    # Flexible constructor to allow for different parameters based on the sprite
    @staticmethod
    def createSprite(name: str, x: int, y: int, x_speed: int = 0, movement_speed: int = 0, y_speed: int = 0, direction: str = "left", threshold: int = 0, image_path: str = "", letter: str = None) -> pygame.sprite.Sprite:
        if name == "Snowball":
            return Snowball(x, y, x_speed, y_speed)
        elif name == "Watcher":
            return Watcher(x, y, direction, threshold)
        elif name == "Player":
            return Player(x, y, movement_speed)
        elif name == "Object":
            return Object(x, y, image_path)
        elif name == "FallingObject":
            return FallingObject(x, y, movement_speed, image_path, letter)
        else:
            raise ValueError("Invalid sprite name")