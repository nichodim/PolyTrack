# Created by Nicholas Seagal, 4/28/2024
# Holds a slot for the powerup menu that is responsible for spawning its powerup when necessary

from powerup import *
from constants import *

class PowerupSlot:
    def __init__(self, type_name, pos):
        self.type_name = type_name

        x, y = pos
        self.rect = pygame.Rect(x, y, SLOT_WIDTH, SLOT_HEIGHT)

        self.spawn_powerup()
    
    def remove_powerup(self):
        self.powerup = None 

        ##############################
        # TODO add timer between these

        self.spawn_powerup()
    
    def spawn_powerup(self):
        pos = self.rect.centerx - TRACK_WIDTH / 2, self.rect.centery - TRACK_HEIGHT / 2
        self.powerup = Powerup(pos, self.type_name)

    def draw(self, game_surf):
        pygame.draw.rect(game_surf, Colors.light_gray, self.rect)
        self.powerup.draw(game_surf)
