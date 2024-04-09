import pygame
from constants import *

class ButtonToggle: # Make this its own file at a later date
    def __init__(self, rect, colors):
        self.rect = rect
        self.colors = colors
        self.toggled = 0
    
    
    # Logic
    def hovered(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        return False
    
    def clicked(self):
        if self.hovered() and pygame.mouse.get_pressed()[0] == 1 and not self.toggled:
            self.toggled = 1
            return True
        return False
    
    def untoggle(self):
        self.toggled = 0


    # Rendering
    def draw(self, game_surf):
        pygame.draw.rect(game_surf, self.colors[self.toggled], self.rect)