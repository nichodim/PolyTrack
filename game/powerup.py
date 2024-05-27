# Use [object].__class__.__name__ elsewhere to compare with effected attachments

import pygame
from constants import Colors, PowerupSprites

class Powerup: # Generic class
    def __init__(self, pos, type_name):
        self.type = PowerUpTypes[type_name]
        self.type_name = type_name
        self.sprite = self.type['sprite']
        self.dimensions = self.type['dimensions']

        x, y = pos[0], pos[1]
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

# Modified by Kelvin Huang
# Add a 'cooldown duration' key to each powerup types determine cooldown duration of each powerup after it is used

PowerUpTypes = { # Actual config
    'bomb': {
        # Generic definitions
        'dimensions': (50, 50),
        'sprite': PowerupSprites.bomb,
        'effected attachments': ['Obstacle', 'Track'], # Empty to effect all

        # Type specific
        'highlight color': Colors.red,
        'blast radius': 1,

        # cooldown
        'cooldown duration': .5
    },
    'bigbomb': {
        # Generic definitions
        'dimensions': (50, 50),
        'sprite': PowerupSprites.bomb_lit,
        'effected attachments': ['Obstacle', 'Track'], # Empty to effect all

        # Type specific
        'highlight color': Colors.red,
        'highlight color': Colors.yellow,
        'blast radius': 2,

        # cooldown
        'cooldown duration': 1
    },
    'slow': {
        # Generic definitions
        'dimensions': (50, 50),
        'sprite': PowerupSprites.slow,
        'effected attachments': [], # Empty to effect all

        # Type specific
        'highlight color': Colors.yellow,
        'time limit': 300, 
        'slow radius': 2,

        # cooldown
        'cooldown duration': 5
    }, 
    'freeze': {
        # Generic definitions
        'dimensions': (50, 50),
        'sprite': PowerupSprites.freeze,
        'effected attachments': [], # Empty to effect all

        # Type specific
        'full freeze strength': 2, 
        'single freeze strength': 5,

        # cooldown
        'cooldown duration': 10
    }
}