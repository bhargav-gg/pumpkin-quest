import pygame
import constants

class Snowball(pygame.sprite.Sprite):
    def __init__(self, x, y, x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load("media/snowball.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
    
    def update(self, collision_group, bar):
        old_x = self.rect.x
        old_y = self.rect.y

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.left < 0 or self.rect.right > constants.WIDTH:
            self.rect.x = old_x
            self.x_speed *= -1
            pygame.mixer.Sound("media/bounce.mp3").play()
        
        if self.rect.top < 0 or self.rect.bottom > constants.HEIGHT:
            self.rect.y = old_y
            self.y_speed *= -1
            pygame.mixer.Sound("media/bounce.mp3").play()
        
        collision = pygame.sprite.spritecollide(self, collision_group, False)

        if collision:
            if self.rect.right < collision[0].rect.right and self.rect.left > collision[0].rect.left:
                self.rect.y = old_y
                self.y_speed *= -1
            else:
                self.rect.x = old_x
                self.x_speed *= -1
            
            if collision[0] != bar:
                collision[0].rect.x = -100
                collision[0].rect.y = -100
                collision[0].kill()

                pygame.mixer.Sound("media/ice breaking.mp3").play()
            else:
                pygame.mixer.Sound("media/bounce.mp3").play()
