import pygame
import constants

#Snowball
class Snowball(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, x, y, x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load("media/snowball.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
    
    #Move snowball
    def update(self, collision_group, bar):
        #Store old position in case of collision
        old_x = self.rect.x
        old_y = self.rect.y

        #Move snowball
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        #Check for collision with screen on left and right
        if self.rect.left < 0 or self.rect.right > constants.WIDTH:
            self.rect.x = old_x
            self.x_speed *= -1
            pygame.mixer.Sound("media/bounce.mp3").play()
        
        #Check for collision with screen on top and bottom
        if self.rect.top < 0 or self.rect.bottom > constants.HEIGHT:
            self.rect.y = old_y
            self.y_speed *= -1
            pygame.mixer.Sound("media/bounce.mp3").play()
        
        #Check for collision with ice block sprites
        collision = pygame.sprite.spritecollide(self, collision_group, False)

        #If collision
        if collision:
            #Check if collision is on top or bottom (if so, reverse y speed)
            if self.rect.right < collision[0].rect.right and self.rect.left > collision[0].rect.left:
                self.rect.y = old_y
                self.y_speed *= -1
            #Else, collision is on left or right (if so, reverse x speed)
            else:
                self.rect.x = old_x
                self.x_speed *= -1
            
            #If collision is with ice block, remove ice block and play sound
            if collision[0] != bar:
                collision[0].rect.x = -100
                collision[0].rect.y = -100
                collision[0].kill()

                pygame.mixer.Sound("media/ice breaking.mp3").play()
            #Else, collision is with bar, play sound
            else:
                pygame.mixer.Sound("media/bounce.mp3").play()
