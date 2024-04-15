import math
import random
import pygame
import track_set_types
from constants import *
from station import Station
from track import Track
from train import Train
from obstacle import Obstacle

class Path:
    def __init__(self, board_tiles, board_rect, end_call, train_type, grid_dimensions, f_pressed=False):
        # Prevents updates on nonexisting game objects
        self.path_initated = False

        # Transfer board info
        self.board_tiles = board_tiles
        self.board_rect = board_rect
        self.end_call = end_call
        self.train_type = train_type
        self.grid_rows, self.grid_cols = grid_dimensions
        self.f_pressed = f_pressed

        # Create path objects
        self.create_stations()
        self.create_station_tracks()
        self.create_train()
        

    def set_f_pressed(self, value):
        self.f_pressed = value
        
    # Creates start and end stations and saves their locations
    # start and end arent positions but are actually tile locatons (col, row)
    def create_stations(self):
        # Find big enough distanced station spots
        
        # check for surrounding station around the random generate point if there is one with in 2 block it will regenerate another one
        def surrounding_station(point):
            col_range = [point[0] - 2, point[0] + 2]
            if col_range[0] < 0: col_range[0] = 0
            if col_range[1] > self.grid_cols - 1: col_range[1] = self.grid_cols - 1

            row_range = [point[1] - 2, point[1] + 2]
            if row_range[0] < 0: row_range[0] = 0
            if row_range[1] > self.grid_rows - 1: row_range[1] = self.grid_rows - 1
            
            for i in range(row_range[0], row_range[1] + 1):
                for j in range(col_range[0], col_range[1] + 1):
                    if isinstance(self.board_tiles[i][j].attached, Station):
                        return True
            return False
        
        # check if train is near the edge of the board
        def near_edge(point):
            return (point[0] < 2 or self.grid_cols - 3 < point[0]) or (point[1] < 2 or self.grid_rows - 3 < point[1])
        
        start, end = (0, 0), (0, 0)

        searching_for_station = True

        # we don't want this while loop to run too much times so if the location is deems semi acceptable it will switch these
        # boolean variable to True so it would generate another of the point
        # point are acceptable if there are no surrounding station within 2 blocks
        # point lean towards the edge of the board preferable at most 2 blocks from the edge
        acceptable_start = False
        acceptable_end = False

        while searching_for_station:
            if acceptable_start == False:
                start = (random.randint(0, self.grid_cols - 1), random.randint(0, self.grid_rows - 1))

            if acceptable_end == False:
                end = (random.randint(0, self.grid_cols - 1), random.randint(0, self.grid_rows - 1))
            
            distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)

            if distance > 4:
                    sur_start = surrounding_station(start)
                    sur_end = surrounding_station(end)

                    if sur_start == False and sur_end == False:
                        searching_for_station = False
                        
                    
                # check if there are station around start position
                    
                    if sur_start == False and near_edge(start):
                        acceptable_start = True

                    if sur_end == False and near_edge(start):
                        acceptable_end = True
                    
                    


        start_image = TrackSprites.start_train_station
        end_image = TrackSprites.end_train_station

        # starting station
        rect_x = self.board_rect.left + OUTER_GAP + start[0] * (TRACK_WIDTH + INNER_GAP)
        rect_y = self.board_rect.top + OUTER_GAP + start[1] * (TRACK_HEIGHT + INNER_GAP)
        station_rect = pygame.Rect(rect_x, rect_y, TRACK_WIDTH, TRACK_HEIGHT)
        self.start_station = Station(
            image = start_image, 
            rect = station_rect, 
            orientation = self.train_orient(start)
        )
        self.board_tiles[start[1]][start[0]].attached = self.start_station

        # ending station
        rect_x = self.board_rect.left + OUTER_GAP + end[0] * (TRACK_WIDTH + INNER_GAP)
        rect_y = self.board_rect.top + OUTER_GAP + end[1] * (TRACK_HEIGHT + INNER_GAP)
        station_rect = pygame.Rect(rect_x, rect_y, TRACK_WIDTH, TRACK_HEIGHT)
        self.end_station = Station(
            image = end_image, 
            rect = station_rect, 
            orientation = self.train_orient(end)
        )
        self.board_tiles[end[1]][end[0]].attached = self.end_station
        
        self.start, self.end = start, end
    
    # Tracks that spawn next to the station based on orientation
    def create_station_tracks(self):
        start_orient = self.start_station.orientation
        self.start_x = int(round(self.start[0] + math.cos(math.radians(start_orient)), 1))
        self.start_y = int(round(self.start[1] - math.sin(math.radians(start_orient)), 1))
        self.create_station_track((self.start_x, self.start_y), start_orient)

        '''
        end_orient = self.end_station.orientation
        end_x = int(round(self.end[0] + math.cos(math.radians(end_orient)), 1))
        end_y = int(round(self.end[1] - math.sin(math.radians(end_orient)), 1))
        self.create_station_track((end_x, end_y), end_orient)
        '''
    
    # Crazy logic I didnt read (thank you Kelvin)
    def create_station_track(self, location, deg):
        possible_tracks = [track_set_types.vertical, track_set_types.horizontal, track_set_types.left, track_set_types.right, track_set_types.ileft, track_set_types.iright]
        if location[0] == 0 or location[0] == self.grid_rows - 1 or deg == 90 or deg == 270:
            possible_tracks.remove(track_set_types.horizontal)
        if location[1] == 0 or location[1] == self.grid_rows - 1 or deg == 0 or deg == 180:
            possible_tracks.remove(track_set_types.vertical)

        if location[0] == 0 or location[1] == self.grid_rows - 1 or deg == 180 or deg == 270:
            possible_tracks.remove(track_set_types.left)
        if location[0] == 0 or location[1] == 0 or deg == 90 or deg == 180:
            possible_tracks.remove(track_set_types.ileft)

        if location[0] == self.grid_rows - 1 or location[1] == self.grid_rows - 1 or deg == 0 or deg == 270:
            possible_tracks.remove(track_set_types.right)
        if location[0] == self.grid_rows - 1 or location[1] == 0 or deg == 0 or deg == 90:
            possible_tracks.remove(track_set_types.iright)
        
        track_rect = pygame.Rect(self.board_tiles[location[1]][location[0]].rect.left, self.board_tiles[location[1]][location[0]].rect.top, TRACK_WIDTH, TRACK_HEIGHT)
        track = Track(track_rect, possible_tracks[random.randint(0, len(possible_tracks) - 1)])
        self.board_tiles[location[1]][location[0]].attached = track
    
    def create_train(self):
        starting_orient = self.start_station.orientation

        # create a list for the train that will store in each cart
        self.train = []
        # build the head for the train
        self.train.append(
            Train(
                type = 'default', 
                board_rect = self.board_rect,
                degree = starting_orient, 
                start = self.start,
                relative_position = "head",
            )
        )

        # multiple cart
        self.total_cart = 5
        self.time = (pygame.Surface.get_width(self.train[0].surface) + 5) / self.train[0].speed
        self.timer = self.time
        print(self.time)


    # Update
    def update(self):
        starting_orient = self.start_station.orientation
        #if self.current_tile and self.train:
        
        for cart in self.train:
            self.check(cart)
            cart.update()
        
        if self.total_cart > 1:
            self.timer -= 1
            if self.timer <= 0:
                self.total_cart -= 1
                self.timer = self.time

                if self.total_cart == 1:
                    self.train.append(
                        Train(
                            type = 'default', 
                            board_rect = self.board_rect,
                            degree = starting_orient, 
                            start = self.start,
                            relative_position = "tail"
                        )
                    )

                else:
                    self.train.append(
                        Train(
                            type = 'default', 
                            board_rect = self.board_rect,
                            degree = starting_orient, 
                            start = self.start
                        )
                    )
        
        if self.f_pressed:
            # adjust the timer and time it takes for a new cart to spawn according to change in speed
            if self.train[0].speed == .15:
                self.timer *= (.15/2.0)
                self.time *= .15/2.0
                print(self.time)

            for train_instance in self.train:
                train_instance.speed = 2.0
            
                
        else:
            # adjust the timer and time it takes for a new cart to spawn according to change in speed 
            if self.train[0].speed != .15:
                self.timer *= 2.0/.15
                self.time = (pygame.Surface.get_width(self.train[0].surface) + 5) / .15

            for train_instance in self.train:
                train_instance.speed = .15


    # Continusly called: checks what to do based on new tiles
    def check(self, cart):
        # declare some helpful variables
        train_width = pygame.Surface.get_width(cart.surface)
        train_height = pygame.Surface.get_height(cart.surface)
        x_no_margin = cart.x - self.board_rect.left - OUTER_GAP
        y_no_margin = cart.y - self.board_rect.top - OUTER_GAP

        x_correction = (train_width/2) * math.cos(math.radians(cart.degree))
        y_correction = (train_width/2) * math.sin(math.radians(cart.degree))        

        # find tile indexes corresponding to train
        front_x = int((x_no_margin + x_correction - INNER_GAP * ((x_no_margin + x_correction) // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
        front_y = int((y_no_margin - y_correction - INNER_GAP * ((y_no_margin - y_correction) // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)

        back_x = int((x_no_margin - x_correction - INNER_GAP * ((x_no_margin - x_correction) // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
        back_y = int((y_no_margin + y_correction - INNER_GAP * ((y_no_margin +  y_correction) // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)
        
        center_x = int((x_no_margin - INNER_GAP * (x_no_margin // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
        center_y = int((y_no_margin - INNER_GAP * (y_no_margin // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)


        # Only cares to end game if train reaches end station
        def find_if_under_station():
            tile = self.board_tiles[center_y][center_x]
            valid_index = (0 <= back_y <= self.grid_cols - 1) and (0 <= back_x <= self.grid_rows - 1) and tile.rect.collidepoint(cart.x - x_correction, cart.y + y_correction)
            if not valid_index: return

            attached_item = self.board_tiles[back_y][back_x].attached
            if attached_item != self.end_station: return

            #correct_direction = round(math.sin(math.radians(cart.degree + 180)), 5) == round(math.sin(math.radians(attached_item.orientation)), 5)
            #if not correct_direction: return

            if cart.relative_position == "tail":
                self.end_call(self, True)
            else: 
                self.train.remove(cart)
        find_if_under_station()

        # Checks next tile for direction
        # Also finds end conditions: True is a failure to find a direction that should not end the path
        def find_new_direction():
            if (center_x, center_y) == cart.current_tile: 
                return (True, 'same tile')

            tile = self.board_tiles[center_y][center_x]
            #if tile == self.current_tile: return (True, 'still on same tile')
            attached_item = tile.attached

            # check if train is on the board and on a tile and not within the gaps
            valid_index = (0 <= center_y <= self.grid_cols - 1) and (0 <= center_x <= self.grid_rows - 1) and tile.rect.collidepoint(cart.x, cart.y) 
            

            if not valid_index: return (True, 'invalid location')            
            
            if attached_item == None: return (False, 'not a track or station')
            if attached_item == self.end_station: return (True, 'ending station')
            if isinstance(attached_item, Obstacle): return (False, 'train crash into obstacle')

            if cart.direction == "forward" and not isinstance(attached_item, Station):
                new_direction = attached_item.directions[int(cart.degree % 360 / 90)]            
                
            else:
                return (True, 'turning')
            if new_direction == 'crash': return (False, 'direction found was not correct for train')

            cart.direction = new_direction
            cart.current_tile = (center_x, center_y)
            #self.current_tile = self.board_tiles[center_y][center_x]
            return(True, 'found new track direction')

        still_fine, condition = find_new_direction()
        if not still_fine: 
            self.end_call(self, False)

    # Dont look here
    def train_orient(self, location):
        orient = [0, 90, 180, 270]
        if location[0] == 0:
            orient.remove(180)
        if location[0] == self.grid_rows - 1:
            orient.remove(0)

        if location[1] == 0:
            orient.remove(90)
        if location[1] == self.grid_cols - 1:
            orient.remove(270)

        return orient[random.randint(0, len(orient) - 1)]
    
    # Deletion of path doesnt leave behind objects
    def __del__(self):
        # delete stations
        col, row = self.start
        self.board_tiles[row][col].attached = None
        col, row = self.end
        self.board_tiles[row][col].attached = None


        self.board_tiles[self.start_y][self.start_x].attached = None
        # delete train
        del self.train

    # Rendering
    def draw(self, game_surf):
        for cart in self.train:
            cart.draw(game_surf)
        
        col, row = self.start
        self.board_tiles[row][col].draw_attached(game_surf)
        col, row = self.end
        self.board_tiles[row][col].draw_attached(game_surf)