# train logic

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
        
    def spawn_train(self, deg, spd, x, y, direction, set):
        trains.append(Train(deg, spd, x, y, direction, set))

    def update(self):
        self.movement()

    def check(self, tiles):
        for i in range(len(trains)):
            # train check tile
            self.tile_x = int((trains[i].x - (board_x + OUTER_GAP + pygame.Surface.get_width(trains[i].surface)/2))//(TRACK_WIDTH + INNER_GAP))
            self.tile_y = int((trains[i].y - (board_y + OUTER_GAP + pygame.Surface.get_height(trains[i].surface)/2))//(TRACK_HEIGHT + INNER_GAP))

            if tiles[self.tile_y][self.tile_x].attached != None:
                self.is_set_same = tiles[self.tile_y][self.tile_x].attached.id == trains[i].set
                self.is_tile_end = tiles[self.tile_y][self.tile_x].attached.point == "end"
                self.is_direction_right = math.sin(math.radians(trains[i].degree + 180)) == math.sin(math.radians(tiles[self.tile_y][self.tile_x].attached.orientation))

                if self.is_set_same & self.is_tile_end & self.is_direction_right:
                    print("Arrived")
        

    def movement(self):
        for i in range(len(trains)):
            self.x_correction = ((TRACK_WIDTH - pygame.Surface.get_width(trains[i].surface)) / 2) * abs(math.sin(math.radians(trains[i].degree)))
            self.y_correction = ((TRACK_HEIGHT - pygame.Surface.get_height(trains[i].surface)) / 2) * abs(math.cos(math.radians(trains[i].degree)))
            
            # turning
            # clockwise
            #print(trains[i].direction)
            self.period = (2 * math.pi * (INNER_GAP + TRACK_WIDTH)) / trains[i].speed 
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
            trains[i].x += trains[i].speed * math.cos(math.radians(trains[i].degree)) 
            trains[i].y += trains[i].speed * -math.sin(math.radians(trains[i].degree))

    def draw(self, game_surf):
        for i in range(len(trains)):
            # draws train on screen
            trains[i].rotate_rect = trains[i].rotate.get_rect(center = (trains[i].x + self.x_correction, trains[i].y + self.y_correction))
            game_surf.blit(trains[i].rotate, trains[i].rotate_rect)
