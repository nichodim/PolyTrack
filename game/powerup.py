# Use [object].__class__.__name__ elsewhere to compare with effected attachments

import pygame
from constants import PowerupSprites

class Powerup: # Generic class
    def __init__(self, pos, type_name):
        self.type = PowerUpTypes[type_name]
        self.type_name = type_name
        self.sprite = self.type['sprite']
        self.dimensions = self.type['dimensions']

        x, y = pos[0] + 7, pos[1] - 7
        w, h = self.dimensions
        self.rect = pygame.Rect(x, y, w, h)
    
    def powerup_over_rect(self, rect):
        positions = [ self.rect.topright, self.rect.topleft, self.rect.bottomright, self.rect.bottomleft ]
        
        for pos in positions:
            side_in_rect = rect.collidepoint(pos)
            if not side_in_rect: return False
        return True

    def set_position_by_center(self, pos):
        delta_x = pos[0] - self.rect.centerx
        delta_y = pos[1] - self.rect.centery
        self.move((delta_x, delta_y))
    def move(self, pos):
        self.rect.move_ip(pos)

    def draw(self, game_surf):
        powerup_scaled = pygame.transform.scale(self.sprite, self.dimensions)
        game_surf.blit(powerup_scaled, self.rect.topleft)

PowerUpTypes = { # Actual config
    'bomb': {
        # Generic definitions
        'dimensions': (50, 50),
        'sprite': PowerupSprites.bomb_lit,
        'effected attachments': [], # Empty to effect all

        # Type specific
        'blast radius': 1
    },
}