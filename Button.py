import pygame

#Source: https://stackoverflow.com/questions/63435298/how-to-create-a-button-class-in-pygame
#Modified by yours truly
class Button:
    #Constructor
    def __init__(self, color, textColor, x, y, width, height, font, text=''):
        self.color = color
        self.textColor = textColor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
    
    #Draw button on screen
    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            text = self.font.render(self.text, 1, self.textColor)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    #Check if mouse is over button
    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
