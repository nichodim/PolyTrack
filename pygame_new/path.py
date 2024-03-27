import math
import random
import pygame
from constants import *
from station import Station
from track import Track
from track_set_types import TrackSetTypes
import track_set_types
from train import Train

class Path:
    def __init__(self, board_tiles, board_rect, end_call):
        self.path_initated = False

        self.board_tiles = board_tiles
        self.board_rect = board_rect

        self.end_call = end_call

        self.create_stations()
        self.create_train()
        self.create_station_tracks()

        self.current_tile = None
        
        self.path_iniated = True

    # start and end arent positions but are actually tile locatons (col, row)
    def create_stations(self):
        distance, i = 0, 0
        start, end = None, None
        while distance < 5:
            start = (random.randint(0, NUM_COLS - 1 - i), random.randint(0 + i, NUM_ROWS - 1))
            end = (random.randint(0, NUM_COLS - 1 - i), random.randint(0 + i, NUM_ROWS - 1))
            i += 1
            if i > NUM_COLS - 1: i = NUM_COLS - 1
            distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        image = TrackSprites.train_station

        # starting station
        rect_x = self.board_rect.left + OUTER_GAP + start[0] * (TRACK_WIDTH + INNER_GAP)
        rect_y = self.board_rect.top + OUTER_GAP + start[1] * (TRACK_HEIGHT + INNER_GAP)
        station_rect = pygame.Rect(rect_x, rect_y, TRACK_WIDTH, TRACK_HEIGHT)
        self.start_station = Station(
            image = image, 
            rect = station_rect, 
            orientation = self.train_orient(start)
        )
        self.board_tiles[start[1]][start[0]].attached = self.start_station

        # ending station
        rect_x = self.board_rect.left + OUTER_GAP + end[0] * (TRACK_WIDTH + INNER_GAP)
        rect_y = self.board_rect.top + OUTER_GAP + end[1] * (TRACK_HEIGHT + INNER_GAP)
        station_rect = pygame.Rect(rect_x, rect_y, TRACK_WIDTH, TRACK_HEIGHT)
        self.end_station = Station(
            image = image, 
            rect = station_rect, 
            orientation = self.train_orient(end)
        )
        self.board_tiles[end[1]][end[0]].attached = self.end_station
        
        self.start, self.end = start, end
    
    def create_station_tracks(self):
        start_orient = self.start_station.orientation
        start_x = int(round(self.start[0] + math.cos(math.radians(start_orient)), 1))
        start_y = int(round(self.start[1] - math.sin(math.radians(start_orient)), 1))
        self.create_station_track((start_x, start_y), start_orient)

        end_orient = self.end_station.orientation
        end_x = int(round(self.end[0] + math.cos(math.radians(end_orient)), 1))
        end_y = int(round(self.end[1] - math.sin(math.radians(end_orient)), 1))
        self.create_station_track((end_x, end_y), end_orient)

    def create_station_track(self, location, deg):
        possible_tracks = [track_set_types.vertical, track_set_types.horizontal, track_set_types.left, track_set_types.right, track_set_types.ileft, track_set_types.iright]
        if location[0] == 0 or location[0] == NUM_ROWS - 1 or deg == 90 or deg == 270:
            possible_tracks.remove(track_set_types.horizontal)
        if location[1] == 0 or location[1] == NUM_ROWS - 1 or deg == 0 or deg == 180:
            possible_tracks.remove(track_set_types.vertical)

        if location[0] == 0 or location[1] == NUM_ROWS - 1 or deg == 180 or deg == 270:
            possible_tracks.remove(track_set_types.left)
        if location[0] == 0 or location[1] == 0 or deg == 90 or deg == 180:
            possible_tracks.remove(track_set_types.ileft)

        if location[0] == NUM_ROWS - 1 or location[1] == NUM_ROWS - 1 or deg == 0 or deg == 270:
            possible_tracks.remove(track_set_types.right)
        if location[0] == NUM_ROWS - 1 or location[1] == 0 or deg == 0 or deg == 90:
            possible_tracks.remove(track_set_types.iright)
        
        track_rect = pygame.Rect(self.board_tiles[location[1]][location[0]].rect.left, self.board_tiles[location[1]][location[0]].rect.top, TRACK_WIDTH, TRACK_HEIGHT)
        track = Track(track_rect, possible_tracks[random.randint(0, len(possible_tracks) - 1)])
        self.board_tiles[location[1]][location[0]].attached = track
    
    def create_train(self):
        starting_orient = self.board_tiles[self.start[1]][self.start[0]].attached.orientation
        self.train = Train(
            type = 'default', 
            degree = starting_orient, 
            tile_location = self.start
        )


    # Update
    def update(self):
        if self.path_iniated and self.train:
            self.check()
            self.train.update()

    def check(self):
        # declare some helpful variables
        train_width = pygame.Surface.get_width(self.train.surface)
        train_height = pygame.Surface.get_height(self.train.surface)
        x_no_margin = self.train.x - self.board_rect.left - OUTER_GAP
        y_no_margin = self.train.y - self.board_rect.top - OUTER_GAP

        x_correction = (train_width/2) * math.cos(math.radians(self.train.degree))
        y_correction = (train_width/2) * math.sin(math.radians(self.train.degree))        

        # find tile indexes corresponding to train
        front_x = int((x_no_margin + x_correction - INNER_GAP * ((x_no_margin + x_correction) // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
        front_y = int((y_no_margin -  y_correction - INNER_GAP * ((y_no_margin - y_correction) // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)

        back_x = int((x_no_margin - x_correction - INNER_GAP * ((x_no_margin - x_correction) // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
        back_y = int((y_no_margin +  y_correction - INNER_GAP * ((y_no_margin +  y_correction) // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)
        
        center_x = int((x_no_margin - INNER_GAP * (x_no_margin // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
        center_y = int((y_no_margin - INNER_GAP * (y_no_margin // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)

        def find_new_direction():
            valid_index = (0 <= center_y <= NUM_ROWS - 1) and (0 <= center_x <= NUM_COLS - 1) and self.board_tiles[center_y][center_x].rect.collidepoint(self.train.x, self.train.y) 
            if not valid_index: return (True, 'was invalid')
            
            tile = self.board_tiles[center_y][center_x]
            if tile == self.current_tile: return (True, 'still on same tile')

            attached_item = tile.attached
            if isinstance(attached_item, Station): return (True, 'was station')
            if not isinstance(attached_item, Track): return (False, 'not track not station')

            new_direction_index = int(round((self.train.degree % 360) / 90))
            if new_direction_index >= len(attached_item.directions): return (False, 'not in length of directions')

            new_direction = attached_item.directions[new_direction_index]
            if new_direction == 'crash': return (False, f'found track was crash direction\n directions: {attached_item.directions}, index: {new_direction_index}, degree: {self.train.degree}, rounded%360: {round((self.train.degree % 360) // 90)}')

            self.train.direction = new_direction
            self.current_tile = self.board_tiles[center_y][center_x]
            return (True, 'worked good')
        
        succeeded, condition = find_new_direction()
        if not succeeded: 
            self.end_call(self, False)
            return

        def find_if_under_station():
            valid_index = (0 <= back_y <= NUM_ROWS - 1) and (0 <= back_x <= NUM_COLS - 1) and self.board_tiles[center_y][center_x].rect.collidepoint(self.train.x - x_correction, self.train.y + y_correction)
            if not valid_index: return

            attached_item = self.board_tiles[back_y][back_x].attached
            if attached_item != self.end_station: return

            correct_direction = round(math.sin(math.radians(self.train.degree + 180)), 5) == round(math.sin(math.radians(attached_item.orientation)), 5)
            if not correct_direction: return
            
            self.end_call(self, True)
        find_if_under_station()
    
    def train_orient(self, location):
        orient = [0, 90, 180, 270]
        if location[0] == 0:
            orient.remove(180)
        if location[0] == NUM_ROWS - 1:
            orient.remove(0)

        if location[1] == 0:
            orient.remove(90)
        if location[1] == NUM_COLS - 1:
            orient.remove(270)

        return orient[random.randint(0, len(orient) - 1)]

    def end_path(self, condition):
        self.end_call(self, condition)
    
    def __del__(self):
        # delete stations
        col, row = self.start
        self.board_tiles[row][col].attached = None
        col, row = self.end
        self.board_tiles[row][col].attached = None

        # delete train
        del self.train

    # Rendering
    def draw(self, game_surf):
        self.train.draw(game_surf)