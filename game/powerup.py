# Use [object].__class__.__name__ elsewhere to compare with effected attachments

import pygame
from constants import EventSprites

class Powerup: # Generic class
    def __init__(self, pos, type_name):
        self.type = PowerUpTypes[type_name]
        self.type_name = type_name

        x, y = pos
        w, h = self.type['dimensions']
        self.rect = pygame.Rect(x, y, w, h)
    
    def set_position_by_center(self, pos):
        delta_x = pos[0] - self.rect.centerx
        delta_y = pos[1] - self.rect.centery
        self.move((delta_x, delta_y))
    def move(self, pos):
        self.rect.move_ip(pos)

    def draw(self, game_surf):
        pygame.blit(game_surf, self.rect.topleft)

PowerUpTypes = { # Actual config
    'bomb': {
        # Generic definitions
        'dimensions': (50, 50),
        'sprite': EventSprites.snowflake_icon,
        'effected attachments': [], # Empty to effect all

        # Type specific
        'blast radius': 2
    },
}