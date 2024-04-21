# Written By Kelvin Huang 
import math
import random
from constants import *

class Wparticles:
    def __init__(self, type, speed, degree, position):
        self.type = type
        self.speed = speed
        self.degree = degree
        self.x = position
        self.y = -(2 + random.random() * 2) if type == "snow" else -(10 + random.random() * 20)
        self.size = -self.y

        if self.type == "rain":
            self.surface = pygame.Surface([5, self.size])
            self.surface.fill(((0,0,255)))
            self.surface.set_colorkey(Colors.white)

            self.rotate = pygame.transform.rotate(self.surface, self.degree)
            self.rotate_rect = self.rotate.get_rect(center = (self.x, self.y))

    def move(self):
        self.x += self.speed * math.sin(self.degree * math.pi/180)
        self.y += self.speed

        if self.x < 0 or GAME_WIDTH < self.x or self.y < GAME_HEIGHT:
            del self 
    
    def draw(self, game_surf):
        if self.type == "snow":
            pygame.draw.circle(game_surf, (255, 255, 255), (self.x, self.y), self.size)
        
        if self.type == "rain":
            self.rotate_rect = self.rotate.get_rect(center = (self.x, self.y))
            game_surf.blit(self.rotate, self.rotate_rect)

        #game_surf.blit(scaled_image_grid, self.rect.topleft)