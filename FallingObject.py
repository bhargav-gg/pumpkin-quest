import pygame
import constants

#Class for objects that fall
class FallingObject(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, x, y, falling_speed, image_path, letter: str = None):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.letter = letter
        self.falling_speed = falling_speed
    
    #Update object (make it fall)
    def update(self):
        self.rect.y += self.falling_speed

        if self.rect.top > constants.HEIGHT:
            self.kill()
