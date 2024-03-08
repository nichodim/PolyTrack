# The board holding and controlling the tiles
import random
import pygame
from constants import *
from tile import Tile
from track import Track
import track_set_types
from obstacle import Obstacle
from station import Station
from trains import Trains
import trains
import math


class Board:
    def __init__(self):
        # Create board
        self.rect = pygame.Rect(board_x, board_y, board_width, board_height)

        # Create tiles
        self.tiles = self.create_grid()
        self.generate_obstacles(random.randint(2, 6))
        self.highlighted_tiles = []

        # Create tile paths - TODO creation should be an event
        #self.tile_paths = []
        #self.create_new_path()
        self.total_paths = 0

    # Board game logic
    def create_grid(self):
        tiles = []
        row_y_increment = TRACK_HEIGHT + INNER_GAP
        row_y = self.rect.top + OUTER_GAP

        for row in range(NUM_ROWS):
            tile_x = OUTER_GAP
            row_list = []
            
            for col in range(NUM_COLS):
                tile_rect = pygame.Rect(self.rect.left + tile_x, row_y, TRACK_WIDTH, TRACK_HEIGHT)
                row_list.append(Tile(tile_rect))
                tile_x += TRACK_WIDTH + INNER_GAP

            tiles.append(row_list)
            row_y += row_y_increment

        return tiles
    
    def generate_obstacles(self, num):
        for n in range(num):
            for m in range(100):
                row = random.randrange(NUM_ROWS)
                col = random.randrange(NUM_COLS)
                tile = self.tiles[row][col]

                attached = tile.attach(Obstacle())
                if attached: break
    
    def unhighlight(self):
        for tile in self.highlighted_tiles:
            tile.highlighted = False
        self.highlighted_tiles = []
    def highlight(self, tiles):
        self.unhighlight()

        for tile in tiles:
            tile.highlighted = True
            self.highlighted_tiles.append(tile)
    
    def update(self, game_surf):
        # for trian
        if self.total_paths < 1:
            self.create_point()
        self.check(game_surf)

    def check(self, game_surf):
        for i in range(len(trains.trains)):
            # declear some helpful variables
            self.train_width = pygame.Surface.get_width(trains.trains[i].surface)
            self.train_height = pygame.Surface.get_height(trains.trains[i].surface)
            self.x_no_margin = trains.trains[i].x - self.rect.left - OUTER_GAP
            self.y_no_margin = trains.trains[i].y - self.rect.top - OUTER_GAP

            self.x_correction = (self.train_width/2) * math.cos(math.radians(trains.trains[i].degree))
            self.y_correction = (self.train_width/2) * math.sin(math.radians(trains.trains[i].degree))        

            # train's front tile
            self.front_x = int((self.x_no_margin + self.x_correction - INNER_GAP * ((self.x_no_margin + self.x_correction) // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
            self.front_y = int((self.y_no_margin - self. y_correction - INNER_GAP * ((self.y_no_margin - self.y_correction) // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)

            self.back_x = int((self.x_no_margin - self.x_correction - INNER_GAP * ((self.x_no_margin - self.x_correction) // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
            self.back_y = int((self.y_no_margin + self. y_correction - INNER_GAP * ((self.y_no_margin + self. y_correction) // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)
            
            self.center_x = int((self.x_no_margin - INNER_GAP * (self.x_no_margin // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
            self.center_y = int((self.y_no_margin - INNER_GAP * (self.y_no_margin // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)

            
            self.valid_index = (0 <= self.center_y <= NUM_ROWS - 1) and (0 <= self.center_x <= NUM_COLS - 1) and self.tiles[self.center_y][self.center_x].rect.collidepoint(trains.trains[i].x, trains.trains[i].y) 

            if self.valid_index and self.tiles[self.center_y][self.center_x].attached != None:
                if self.tiles[self.center_y][self.center_x].attached.type == "track":
                    if trains.trains[i].degree % 360 == 0 and self.tiles[self.center_y][self.center_x].attached.d0 != "crash":
                        trains.trains[i].direction = self.tiles[self.center_y][self.center_x].attached.d0
                    elif trains.trains[i].degree % 360 == 90 and self.tiles[self.center_y][self.center_x].attached.d90 != "crash":
                        trains.trains[i].direction = self.tiles[self.center_y][self.center_x].attached.d90
                    elif trains.trains[i].degree % 360 == 180 and self.tiles[self.center_y][self.center_x].attached.d180 != "crash":
                        trains.trains[i].direction = self.tiles[self.center_y][self.center_x].attached.d180
                    elif trains.trains[i].degree % 360 == 270 and self.tiles[self.center_y][self.center_x].attached.d270 != "crash":
                        trains.trains[i].direction = self.tiles[self.center_y][self.center_x].attached.d270

            self.valid_index = (0 <= self.back_y <= NUM_ROWS - 1) and (0 <= self.back_x <= NUM_COLS - 1) and self.tiles[self.center_y][self.center_x].rect.collidepoint(trains.trains[i].x - self.x_correction, trains.trains[i].y + self.y_correction)
            # detect if train enter the station
            if self.valid_index and self.tiles[self.back_y][self.back_x].attached != None:
                attached_item = self.tiles[self.back_y][self.back_x].attached
                if isinstance(attached_item, Station):
                    self.is_set_same = self.tiles[self.back_y][self.back_x].attached.id == trains.trains[i].set
                    self.is_tile_end = self.tiles[self.back_y][self.back_x].attached.point == "end"
                    self.is_direction_right = round(math.sin(math.radians(trains.trains[i].degree + 180)), 5) == round(math.sin(math.radians(self.tiles[self.back_y][self.back_x].attached.orientation)), 5)

                    if self.is_set_same & self.is_tile_end & self.is_direction_right:
                        print("Arrived")
                        # remove train and stations and respawn it somewhere else on the board
                        self.x, self.y = trains.trains[i].start
                        self.tiles[self.y][self.x].attached = None
                        self.x, self.y = trains.trains[i].end
                        self.tiles[self.y][self.x].attached = None
                        trains.trains.pop(i)
                        self.total_paths -= 1

    def create_point(self):
        # randomly generate 2 set of coordinate from (0, 0) to (NUM_COLS - 1, NUM_ROWS - 1)
        
        self.distance = 0
        self.i = 0
        while self.distance < 5:
            self.start = (random.randint(0, NUM_COLS - 1 - self.i), random.randint(0 + self.i, NUM_ROWS - 1))
            self.end = (random.randint(0, NUM_COLS - 1 - self.i), random.randint(0 + self.i, NUM_ROWS - 1))
            self.i += 1
            if self.i > NUM_COLS - 1:
                self.i = NUM_COLS - 1
            self.distance = math.sqrt((self.end[0] - self.start[0])**2 + (self.end[1] - self.start[1])**2)
        
        # determine orientation for locations
        #self.start = (9, 0)
        #self.end = (0, 0)

        # starting location
        image = TrackSprites.train_station
        point_rect = pygame.Rect(self.rect.left + OUTER_GAP + self.start[0] * (TRACK_WIDTH + INNER_GAP), self.rect.top + OUTER_GAP + self.start[1] * (TRACK_HEIGHT + INNER_GAP) , TRACK_WIDTH, TRACK_HEIGHT)

        start_station = Station(
            image = image, 
            rect = point_rect, 
            point = 'start', 
            orientation = self.train_orient(self.start),
            id = self.total_paths
        )
        self.tiles[self.start[1]][self.start[0]].attached = start_station

        # add initial track
        self.initial_track((int(self.start[0] + math.cos(math.radians(start_station.orientation))), int(self.start[1] - math.sin(math.radians(start_station.orientation)))), start_station.orientation)
        
        # ending location
        point_rect = pygame.Rect(self.rect.left + OUTER_GAP + self.end[0] * (TRACK_WIDTH + INNER_GAP), self.rect.top + OUTER_GAP + self.end[1] * (TRACK_HEIGHT + INNER_GAP) , TRACK_WIDTH, TRACK_HEIGHT)
        end_station = Station(
            image = image, 
            rect = point_rect, 
            point = 'end', 
            orientation = self.train_orient(self.end),
            id = self.total_paths
        )
        self.tiles[self.end[1]][self.end[0]].attached = end_station
        
        # add initial track
        self.initial_track((int(self.end[0] + math.cos(math.radians(end_station.orientation))), int(self.end[1] - math.sin(math.radians(end_station.orientation)))), end_station.orientation)

        # spawn_train(degree, speed, x, y, direction)
        # direction could be "forward", "clockwise", or "counter-clockwise"

        Trains().spawn_train(self.tiles[self.start[1]][self.start[0]].attached.orientation, 1, self.start[0], self.start[1], "forward", self.total_paths, self.start, self.end)
        self.total_paths += 1

    def train_orient(self, location):
        # if x = 0 orient can't be w
        # if x = 9 orient can't be e
        # if y = 0 orient can't be n
        # if y = 9 orient can't be s

        self.orient = [0, 90, 180, 270]
        if location[0] == 0:
            self.orient.remove(180)
        if location[0] == NUM_ROWS - 1:
            self.orient.remove(0)

        if location[1] == 0:
            self.orient.remove(90)
        if location[1] == NUM_COLS - 1:
            self.orient.remove(270)

        return self.orient[random.randint(0, len(self.orient) - 1)]
    
    def initial_track(self, location, deg):
        self.possible_tracks = [track_set_types.vertical, track_set_types.horizontal, track_set_types.left, track_set_types.right, track_set_types.ileft, track_set_types.iright]
        if location[0] == 0 or location[0] == NUM_ROWS - 1 or deg == 90 or deg == 270:
            self.possible_tracks.remove(track_set_types.horizontal)
        if location[1] == 0 or location[1] == NUM_ROWS - 1 or deg == 0 or deg == 180:
            self.possible_tracks.remove(track_set_types.vertical)


        if location[0] == 0 or location[1] == NUM_ROWS - 1 or deg == 180 or deg == 270:
            self.possible_tracks.remove(track_set_types.left)
        if location[0] == 0 or location[1] == 0 or deg == 90 or deg == 180:
            self.possible_tracks.remove(track_set_types.ileft)

        if location[0] == NUM_ROWS - 1 or location[1] == NUM_ROWS - 1 or deg == 0 or deg == 270:
            self.possible_tracks.remove(track_set_types.right)
        if location[0] == NUM_ROWS - 1 or location[1] == 0 or deg == 0 or deg == 90:
            self.possible_tracks.remove(track_set_types.iright)
        print(location)
        
        self.track_rect = pygame.Rect(self.tiles[location[1]][location[0]].rect.left, self.tiles[location[1]][location[0]].rect.top, TRACK_WIDTH, TRACK_HEIGHT)
        self.track = Track(self.track_rect, self.possible_tracks[random.randint(0, len(self.possible_tracks) - 1)])
        self.tiles[location[1]][location[0]].attached = self.track

    # TODO calculation does not work on grids that arent 10 by 10
    def find_tile_in_location(self, pos):
        x, y = pos

        y_no_margin = y - self.rect.top - OUTER_GAP
        row = int((y_no_margin - INNER_GAP * (y_no_margin // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
        
        x_no_margin = x - self.rect.left - OUTER_GAP
        col = int((x_no_margin - INNER_GAP * (x_no_margin // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)

        if ( 
            0 <= row <= NUM_ROWS - 1 and # valid row
            0 <= col <= NUM_COLS - 1 and # valid column
            self.tiles[row][col].rect.collidepoint(pos) # over tile
        ):
            return self.tiles[row][col]
        return None
    
    # Rendering
    def draw(self, game_surf):
        self.draw_board(game_surf)
        self.draw_tiles(game_surf)
        #self.draw_path_tiles(game_surf)
        self.draw_tile_items(game_surf)
        
    def draw_board(self, game_surf):
        pygame.draw.rect(game_surf, Colors.light_gray, self.rect)

    def draw_tiles(self, game_surf):
        for row in self.tiles:
            for tile in row:
                if tile.highlighted:
                    pygame.draw.rect(game_surf, Colors.green, tile.rect)
                else: 
                    pygame.draw.rect(game_surf, Colors.white, tile.rect)

    def draw_tile_items(self, game_surf):
        for row in self.tiles:
            for tile in row:
                tile.draw_attached(game_surf)
