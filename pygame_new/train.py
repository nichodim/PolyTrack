# train logic

import pygame
import math
from constants import *
from board import Board

class Train:
    def __init__(self):
        self.board_x = GAME_WIDTH / 2 - (NUM_COLS * TRACK_WIDTH + INNER_GAP * (NUM_COLS - 1) + OUTER_GAP * 2) / 2
        self.board_y = GAME_HEIGHT * 0.1
        self.trains = []
        
        self.train = {}
        
        # pygame.Surface([width,height]) controls size of the train
        self.train["area"] = pygame.Surface([60, 48])
        self.train["degree"] = 0
        self.train["speed"] = 1
        #print(self.train["area"].get_width)

        # center of the train x and y location
        self.train["location_x"] = self.board_x + OUTER_GAP + pygame.Surface.get_width(self.train["area"])/2 
        self.train["location_y"] = self.board_y + OUTER_GAP + pygame.Surface.get_height(self.train["area"])/2 + (TRACK_HEIGHT - pygame.Surface.get_height(self.train["area"]))/2

        self.train["rotated"] = pygame.transform.rotate(self.train["area"], self.train["degree"])
        self.train["rotated_rect"] = self.train["rotated"].get_rect(center = (self.train["location_x"], self.train["location_y"]))
        
        # there are three option for this "foward", clockwise", and "counter-clockwise"
        # "foward" makes the train keep moving in the direction its facing
        # "clockwise" makes the train turn clockwise
        # "counter-clockwise" makes the train turn counter-clockwise
        self.train["direction"] = "clockwise"
        
        # makes it background it on transparent so it looks like it turning and it would look like it expanding
        self.train["area"].set_colorkey(Colors.white)

        # train image
        image = TrackSprites.horizontal_track.convert_alpha()
        image = pygame.transform.smoothscale(image, (56, 48)) 
        self.train["area"].blit(image, (0,0))

        self.trains.append(self.train)



    def spawn_train(self):
        self.train = {"area": pygame.Rect(50, 50, 100, 50), "speed": 1, "degree": 0.0}
        self.trains.append(self.train)

    def draw(self, game_surf):
        
        for i in range(len(self.trains)):
            # turning
            # clockwise
            if self.trains[i]["direction"] == "clockwise":
                self.trains[i]["degree"] -= self.trains[i]["speed"] # minus 1 to the degree since it going counter-clockwise
            
            # counter-clockwise
            if self.trains[i]["direction"] == "counter-clockwise":
                self.trains[i]["degree"] += self.trains[i]["speed"] # add 1 to the degree since it going counter-clockwise
            
            #print(self.trains[i]["degree"] % 90 == 0)
            if self.trains[i]["degree"] % 90 < self.trains[i]["speed"]: # check when it full turns
                self.trains[i]["direction"] = "foward" # stop it from turning
                self.trains[i]["degree"] -= self.trains[i]["degree"] % 90
            # update the turn on screen
            self.trains[i]["rotated"] = pygame.transform.rotate(self.trains[i]["area"], self.trains[i]["degree"])

            #print(self.trains[i]["degree"])

            # movement
            self.trains[i]["location_x"] += self.trains[i]["speed"] * math.cos(math.radians(self.trains[i]["degree"]))
            self.trains[i]["location_y"] += self.trains[i]["speed"] * -math.sin(math.radians(self.trains[i]["degree"]))

            # draws it on screen
            self.trains[i]["rotated_rect"] = self.trains[i]["rotated"].get_rect(center = (self.train["location_x"], self.train["location_y"]))
            game_surf.blit(self.trains[i]["rotated"], self.trains[i]["rotated_rect"])

