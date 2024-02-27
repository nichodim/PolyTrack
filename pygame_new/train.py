# handles individual train data

import pygame
from constants import *
import random

class Train:
    def __init__(self, deg, spd, x, y, direction):
         # pygame.Surface([width,height]) controls size of the train
        self.surface = pygame.Surface([60, 48])
        self.degree = deg
        self.speed = spd
        
        # center of the train x and y location
        self.x = board_x + OUTER_GAP + pygame.Surface.get_width(self.surface)/2 + x * (TRACK_WIDTH + INNER_GAP)
        self.y = board_y + OUTER_GAP + pygame.Surface.get_height(self.surface)/2 + y * (TRACK_HEIGHT + INNER_GAP) 

        # there are three option for this "foward", clockwise", and "counter-clockwise"
        # "foward" makes the train keep moving in the direction its facing
        # "clockwise" makes the train turn clockwise
        # "counter-clockwise" makes the train turn counter-clockwise
        self.direction = direction

        self.rotate = pygame.transform.rotate(self.surface, self.degree)
        self.rotate_rect = self.rotate.get_rect(center = (self.x, self.y))

        # makes it background it on transparent so it looks like it turning and it would look like it expanding
        self.surface.set_colorkey(Colors.white)

        # train image
        #image = TrackSprites.red_train.convert_alpha()
        #image = pygame.transform.smoothscale(image, (56, 48)) 
        #self.surface.blit(image, (0,0))
        
        image = random.choice(TrackSprites.random_train_choice).convert_alpha()
        image = pygame.transform.smoothscale(image, (56, 48)) 
        self.surface.blit(image, (0,0))