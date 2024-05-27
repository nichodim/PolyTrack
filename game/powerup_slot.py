# Created by Nicholas Seagal, 4/28/2024
# Holds a slot for the powerup menu that is responsible for spawning its powerup when necessary

from powerup import *
from constants import *
from timer import Timer

class PowerupSlot:
    def __init__(self, type_name, pos):
        self.type_name = type_name

        x, y = pos
        self.rect = pygame.Rect(x, y, SLOT_WIDTH, SLOT_HEIGHT)
        self.timer = None
        self.spawn_powerup()
    
    def remove_powerup(self):        
        x = self.rect.left + SLOT_WIDTH/2                                   # Modified by Kelvin Huang, May 26, 2024
        y = self.rect.top + SLOT_HEIGHT/2                                   # Add cooldown to each powerup, duration can be adjust in powerup.py
        r = SLOT_WIDTH/2
        self.timer = Timer(x, y, r, PowerUpTypes[self.type_name]['cooldown duration'], alpha=100)

        #print("powerup on cooldown")
        self.spawn_powerup()

    def spawn_powerup(self):
        pos = self.rect.centerx - TRACK_WIDTH / 2, self.rect.centery - TRACK_HEIGHT / 2
        self.powerup = Powerup(pos, self.type_name)

    def draw(self, game_surf):
        pygame.draw.rect(game_surf, Colors.light_gray, self.rect)
        self.powerup.draw(game_surf)


        if self.timer != None:                                              # Modified by Kelvin Huang, May 26, 2024
            self.timer.draw(game_surf)                                      # Draw timer if timer exist and tick the time
            if self.timer.tick(): self.timer = None
