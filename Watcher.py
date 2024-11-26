import pygame

#Watcher class
class Watcher(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, x, y, direction, threshold):
        super().__init__()
        self.direction = direction
        self.image = pygame.image.load(f"media/watcher_{self.direction}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame_count = 0
        self.threshold = threshold
    
    #Move watcher (make it change directions)
    def update(self):
        #Increment frame count
        self.frame_count += 1
        
        #If frame count reaches threshold, change direction
        if self.frame_count == self.threshold:
            self.frame_count = 0
            offset = 70

            #Change direction
            if self.direction == "left":
                self.direction = "right"
                self.rect.x += offset
            elif self.direction == "right":
                self.direction = "left"
                self.rect.x -= offset
            elif self.direction == "forward":
                self.direction = "backward"
                self.rect.y += offset
            elif self.direction == "backward":
                self.direction = "forward"
                self.rect.y -= offset
            
            #Update image for new direction
            self.image = pygame.image.load(f"media/watcher_{self.direction}.png")
        
