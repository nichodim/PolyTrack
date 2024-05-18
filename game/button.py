# Button Class
import pygame
from constants import SFX

class Button: # Make this its own file at a later date
    def __init__(self, x, y, image, scale):
        self.scale = scale
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image,(int(self.width * scale), int(self.height * scale)))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    
    # Logic
    def hovered(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        return False
    
    def clicked(self):
        if self.hovered() and pygame.mouse.get_pressed()[0] == 1:
            SFX.bleep.play()
            return True
        return False

    def setImage(self, image):
        self.image = pygame.transform.scale(image,(int(self.width * self.scale), int(self.height * self.scale)))


    # Rendering
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
