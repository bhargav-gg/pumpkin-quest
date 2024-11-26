import pygame

#Object that does not move
class Object(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    #Object does not move
    def update(self):
        pass