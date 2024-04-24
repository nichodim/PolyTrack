# handles individual train data

import pygame
from constants import *
from board_item_types import TrainTypes
import math

class Train:
    def __init__(self, type, board_rect, degree, start, speed = 'default'):
        data = TrainTypes[type]
        self.board_rect = board_rect
        self.image = data['image']

        if speed == 'default': self.speed = data['speed']
        else: self.speed = speed

        self.default_speed = data['speed']
        
        self.direction, self.degree = "forward", degree
        self.current_tile = start

        # Make expanding surface/image with transparent background
        self.surface = pygame.Surface([60 * (TRACK_WIDTH/50), (TRACK_HEIGHT - 2 * (TRACK_HEIGHT/50))])
        self.surface.set_colorkey(Colors.white)
        self.image = pygame.transform.smoothscale(self.image, [60 * (TRACK_WIDTH/50), 48 * (TRACK_HEIGHT/50)])
        self.surface.blit(self.image, (0,0))
        
        self.set_pos(start)

        self.rotate = pygame.transform.rotate(self.surface, self.degree)
        self.rotate_rect = self.rotate.get_rect(center = (self.x, self.y))

    # Uses tile location + angle to find x, y coordinates
    def set_pos(self, start):
        col, row = start
        self.x_center_adjustment = abs(pygame.Surface.get_width(self.surface) / 2 * math.cos(math.radians(self.degree)) + pygame.Surface.get_height(self.surface) / 2 * math.sin(math.radians(self.degree)))
        self.y_center_adjustment = abs(pygame.Surface.get_height(self.surface) / 2 * math.cos(math.radians(self.degree)) + pygame.Surface.get_width(self.surface) / 2 * math.sin(math.radians(self.degree)))
        
        self.x = self.board_rect.left + OUTER_GAP + col * (TRACK_WIDTH + INNER_GAP) + self.x_center_adjustment
        self.y = self.board_rect.top + OUTER_GAP + row * (TRACK_HEIGHT + INNER_GAP) + self.y_center_adjustment
        if self.degree == 180:
            self.x -= pygame.Surface.get_width(self.surface) - TRACK_WIDTH - INNER_GAP
        if self.degree == 90:
            self.y -= pygame.Surface.get_width(self.surface) - TRACK_HEIGHT - INNER_GAP
    

    # Update Section
    def update(self):
        self.update_speed()
        self.move()

    # Sappropriately alters speed if the train is turning
    def update_speed(self):
        if self.direction == 'forward' or self.direction == 'crash': return

        self.period = (2 * math.pi * (TRACK_WIDTH/2)*(50/50)) / self.speed 

        if self.direction == "clockwise":
            self.degree -= 360 / self.period #  minus degree since it going counter-clockwise

        # counter-clockwise
        if self.direction == "counter-clockwise":
            self.degree += 360 / self.period # add degree since it going counter-clockwise
        
        # the following if statement is used it case the speed is a number that not a factor of 90            
        if round(self.degree % 90, 5) < round(360 / self.period, 5): # check when it close full turns
            self.direction = "forward" # stop it from turning
            self.degree -= self.degree % 90 # correct it

        # update the turn on screen
        self.rotate = pygame.transform.rotate(self.surface, self.degree)
    
    def move(self):
        self.x += self.speed * math.cos(math.radians(self.degree)) 
        self.y += self.speed * -math.sin(math.radians(self.degree))

    # Rendering
    def draw(self, game_surf):
        y_correction = (TRACK_HEIGHT - pygame.Surface.get_height(self.surface)) / 2 * abs(math.cos(math.radians(self.degree)))
        x_correction = (TRACK_HEIGHT - pygame.Surface.get_height(self.surface)) / 2 * abs(math.sin(math.radians(self.degree)))

        self.rotate_rect = self.rotate.get_rect(center = (self.x, self.y + y_correction))
        game_surf.blit(self.rotate, self.rotate_rect)