# Written By Kelvin Huang, April 21, 2024
# set up foundation of object
import math
import random
from constants import *

class Wparticles:
    def __init__(self, type, speed, degree, position):
        self.type = type
        self.speed = speed
        self.degree = degree
        self.x = position
        # adjust y position so it out of the screen
        self.y = -(2 + random.random() * 2) if type == "snow" else -(10 + random.random() * 20)
        self.size = -self.y

        if self.type == "rain":
            # set up surface
            self.surface = pygame.Surface([5, self.size])
            # color of the rain drops
            self.surface.fill(((0,0,255)))
            self.surface.set_colorkey(Colors.white)

            # rotation of the rain
            self.rotate = pygame.transform.rotate(self.surface, self.degree)
            self.rotate_rect = self.rotate.get_rect(center = (self.x, self.y))

    def move(self):
        # moved object
        self.x += self.speed * math.sin(self.degree * math.pi/180)
        self.y += self.speed

        # delete object if out of screen
        if self.x < 0 or GAME_WIDTH < self.x or self.y < GAME_HEIGHT:
            del self 
    
    def draw(self, game_surf):
        # draw for snow
        if self.type == "snow":
            pygame.draw.circle(game_surf, (255, 255, 255), (self.x, self.y), self.size)
        
        # draw for rain
        if self.type == "rain":
            self.rotate_rect = self.rotate.get_rect(center = (self.x, self.y))
            game_surf.blit(self.rotate, self.rotate_rect)
