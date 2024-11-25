import pygame
import constants

class Letter(pygame.sprite.Sprite):
    def __init__(self, x, y, letter, falling_speed):
        super().__init__()
        self.image = pygame.image.load(f"media/{letter}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.letter = letter
        self.falling_speed = falling_speed

    def update(self):
        self.rect.y += self.falling_speed
