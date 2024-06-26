# train logic
# Depracated

import pygame
import math
from constants import *
#from board import Board
from train import Train

trains = []
class Trains:
    def __init__(self):
        #self.spawn_train(180, 1, 5, 5, "counter-clockwise")
        pass
        
    def spawn_train(self, deg, spd, x, y, direction, set, start, end):
        trains.append(Train(deg, spd, x, y, direction, set, start, end))

    def update(self):
        self.movement()

    def movement(self):
        for i in range(len(trains)):
            # turning
            # clockwise
            #print(trains[i].direction)
            if trains[i].direction == "clockwise" or trains[i].direction == "counter-clockwise":
                self.period = (2 * math.pi * (TRACK_WIDTH/2)*(50/50)) / trains[i].speed 
                if trains[i].direction == "clockwise":
                    trains[i].degree -= 360 / self.period #  minus degree since it going counter-clockwise

                # counter-clockwise
                if trains[i].direction == "counter-clockwise":
                    trains[i].degree += 360 / self.period # add degree since it going counter-clockwise
                
                # the following if statement is used it case the speed is a number that not a factor of 90            
                if round(trains[i].degree % 90, 5) < round(360 / self.period, 5): # check when it close full turns
                    trains[i].direction = "foward" # stop it from turning
                    trains[i].degree -= trains[i].degree % 90 # correct it


            # update the turn on screen
            trains[i].rotate = pygame.transform.rotate(trains[i].surface, trains[i].degree)

            # movement
            if trains[i].direction != "crash":
                trains[i].x += trains[i].speed * math.cos(math.radians(trains[i].degree)) 
                trains[i].y += trains[i].speed * -math.sin(math.radians(trains[i].degree))

    def draw(self, game_surf):
        for i in range(len(trains)):
            # draws train on screen
            
            self.y_correction = (TRACK_HEIGHT - pygame.Surface.get_height(trains[i].surface)) / 2 * abs(math.cos(math.radians(trains[i].degree)))

            trains[i].rotate_rect = trains[i].rotate.get_rect(center = (trains[i].x, trains[i].y + self.y_correction))
            game_surf.blit(trains[i].rotate, trains[i].rotate_rect)
