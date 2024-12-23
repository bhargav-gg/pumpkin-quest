import pygame
import constants

#Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load("media/sprite_backward_idle.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.last_direction = "right"
        self.frame_count = 0
        self.time_frame = 0

    #Regular update function, dictates player sprite movement (in regular context)
    def update(self, collision_group):
        pressed_keys = pygame.key.get_pressed()

        #Key press detection (WASD and arrow keys)
        pressed_left = pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]
        pressed_right = pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]
        pressed_up = pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]
        pressed_down = pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]

        #x, y values before movement in case of collision
        old_x = self.rect.x
        old_y = self.rect.y

        #Move player
        if pressed_left:
            self.rect.x -= self.speed
            
            if self.last_direction != "left":
                self.frame_count = 0
                self.time_frame = 0
                self.last_direction = "left"
            else:
                self.time_frame += 1

                if self.time_frame % 10 == 0:
                    self.frame_count += 1
                self.frame_count %= 6
        elif pressed_right:
            self.rect.x += self.speed
            
            if self.last_direction != "right":
                self.frame_count = 0
                self.time_frame = 0
                self.last_direction = "right"
            else:
                self.time_frame += 1

                if self.time_frame % 10 == 0:
                    self.frame_count += 1
                self.frame_count %= 6
        elif pressed_up:
            self.rect.y -= self.speed
            
            if self.last_direction != "forward":
                self.frame_count = 0
                self.time_frame = 0
                self.last_direction = "forward"
            else:
                self.time_frame += 1

                if self.time_frame % 10 == 0:
                    self.frame_count += 1
                self.frame_count %= 6
        elif pressed_down:
            self.rect.y += self.speed
            
            if self.last_direction != "backward":
                self.frame_count = 0
                self.time_frame = 0
                self.last_direction = "backward"
            else:
                self.time_frame += 1

                if self.time_frame % 10 == 0:
                    self.frame_count += 1
                self.frame_count %= 6
        else:
            self.frame_count = 0
            self.time_frame = 0
        
        #Idle animation
        if not pressed_left and not pressed_right and not pressed_up and not pressed_down:
            self.image = pygame.image.load(f"media/sprite_{self.last_direction}_idle.png")
            self.time_frame = 0
        else:
            self.image = pygame.image.load(f"media/sprite_{self.last_direction}_walk{self.frame_count}.png")
        
        #Collision detection
        #Revert to old x, y values if collision detected
        if pygame.sprite.spritecollide(self, collision_group, False) or self.rect.x < 0 or self.rect.x > constants.WIDTH - self.rect.width or self.rect.y < 0 or self.rect.y > constants.HEIGHT - self.rect.height:
            self.rect.x = old_x
            self.rect.y = old_y
            self.image = pygame.image.load(f"media/sprite_{self.last_direction}_idle.png")
    
    #Update function for player sprite movement (two-directional, Christmas level)
    def update_left_right(self):
        pressed_keys = pygame.key.get_pressed()

        #Key press detection (A and D/left and right arrow keys)
        pressed_left = pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]
        pressed_right = pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]

        #x value before movement in case of collision
        old_x = self.rect.x

        #Move player
        if pressed_left:
            self.rect.x -= self.speed
            
            if self.last_direction != "left":
                self.frame_count = 0
                self.time_frame = 0
                self.last_direction = "left"
            else:
                self.time_frame += 1

                if self.time_frame % 10 == 0:
                    self.frame_count += 1
                self.frame_count %= 6
        elif pressed_right:
            self.rect.x += self.speed
            
            if self.last_direction != "right":
                self.frame_count = 0
                self.time_frame = 0
                self.last_direction = "right"
            else:
                self.time_frame += 1

                if self.time_frame % 10 == 0:
                    self.frame_count += 1
                self.frame_count %= 6
        else:
            self.frame_count = 0
            self.time_frame = 0
        
        #Idle animation
        if not pressed_left and not pressed_right:
            self.image = pygame.image.load(f"media/sprite_{self.last_direction}_idle.png")
            self.time_frame = 0
        else:
            self.image = pygame.image.load(f"media/sprite_{self.last_direction}_walk{self.frame_count}.png")
        
        #Collision detection with walls, revert to old x value if collision detected
        if self.rect.x < 0 or self.rect.x > constants.WIDTH - self.rect.width:
            self.rect.x = old_x
            self.image = pygame.image.load(f"media/sprite_{self.last_direction}_idle.png")
        