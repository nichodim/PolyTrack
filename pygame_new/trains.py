# train logic

import pygame
import math
from constants import *
from board import Board
from train import Train

trains = []
class Trains:
    def __init__(self):
        self.spawn_train(0, 1, 5, 5, "counter-clockwise")
        
    def spawn_train(self, deg, spd, x, y, direction):
        trains.append(Train(deg, spd, x, y, direction))

    def draw(self, game_surf):
        
        for i in range(len(trains)):
            # turning
            # clockwise
            if trains[i].direction == "clockwise":
                trains[i].degree -= trains[i].speed # minus 1 to the degree since it going counter-clockwise
            
            # counter-clockwise
            if trains[i].direction == "counter-clockwise":
                trains[i].degree += trains[i].speed # add 1 to the degree since it going counter-clockwise
            
            #print(trains[i]["degree"] % 90 == 0)
            if trains[i].degree % 90 < trains[i].speed: # check when it full turns
                trains[i].direction = "foward" # stop it from turning
                trains[i].degree -= trains[i].degree % 90


            # update the turn on screen
            trains[i].rotate = pygame.transform.rotate(trains[i].surface, trains[i].degree)

            # movement
            trains[i].x += trains[i].speed * math.cos(math.radians(trains[i].degree)) # * 1.05 seems like this will make it center when turn
            trains[i].y += trains[i].speed * -math.sin(math.radians(trains[i].degree))


            self.x_correction = ((TRACK_WIDTH - pygame.Surface.get_width(trains[i].surface)) / 2) * abs(math.sin(math.radians(trains[i].degree)))
            self.y_correction = ((TRACK_HEIGHT - pygame.Surface.get_height(trains[i].surface)) / 2) * abs(math.cos(math.radians(trains[i].degree)))
            print(self.x_correction, self.y_correction)

            # draws it on screen
            trains[i].rotate_rect = trains[i].rotate.get_rect(center = (trains[i].x + self.x_correction, trains[i].y + self.y_correction))
            game_surf.blit(trains[i].rotate, trains[i].rotate_rect)

