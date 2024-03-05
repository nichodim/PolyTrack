# The board holding and controlling the tiles
import random
import pygame
from constants import *
from tile import Tile
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
    
    def update(self):
        # for trian
        if self.total_paths < 1:
            self.create_point()
        self.check()

    def check(self):
        for i in range(len(trains.trains)):
            # train check tile
            
            # train's back tile
            self.back_x = int((trains.trains[i].x - (board_x + OUTER_GAP + pygame.Surface.get_width(trains.trains[i].surface)/2) + pygame.Surface.get_width(trains.trains[i].surface) * ((-math.cos(math.radians(trains.trains[i].degree)) + 1)//2)) // (TRACK_WIDTH + INNER_GAP))
            self.back_y = int((trains.trains[i].y - (board_y + OUTER_GAP + pygame.Surface.get_height(trains.trains[i].surface)/2) + pygame.Surface.get_width(trains.trains[i].surface) * ((math.sin(math.radians(trains.trains[i].degree)) + 1)//2)) // (TRACK_HEIGHT + INNER_GAP))

            # train's front tile
            self.front_x = int((trains.trains[i].x - (board_x + OUTER_GAP + pygame.Surface.get_width(trains.trains[i].surface)/2) + pygame.Surface.get_width(trains.trains[i].surface) * ((math.cos(math.radians(trains.trains[i].degree)) + 1)//2)) // (TRACK_WIDTH + INNER_GAP))
            self.front_y = int((trains.trains[i].y - (board_y + OUTER_GAP + pygame.Surface.get_height(trains.trains[i].surface)/2) + pygame.Surface.get_width(trains.trains[i].surface) * ((-math.sin(math.radians(trains.trains[i].degree)) + 1)//2)) // (TRACK_HEIGHT + INNER_GAP))

            self.valid_index = (0 <= self.back_y <= NUM_ROWS - 1) and (0 <= self.back_x <= NUM_COLS - 1)
            # detect if train enter the station
            if self.valid_index and self.tiles[self.back_y][self.back_x].attached != None:

                if self.tiles[self.back_y][self.back_x].attached.type == "station":
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
        
            self.valid_index = (0 <= self.front_y <= NUM_ROWS - 1) and (0 <= self.front_x <= NUM_COLS - 1)
            if self.valid_index and self.tiles[self.front_y][self.front_x].attached != None:
                if self.tiles[self.front_y][self.front_x].attached.type == "track":
                    if trains.trains[i].degree == 0:
                        trains.trains[i].direction = self.tiles[self.front_y][self.front_x].attached.d0
                    elif trains.trains[i].degree == 90:
                        trains.trains[i].direction = self.tiles[self.front_y][self.front_x].attached.d90
                    elif trains.trains[i].degree == 180:
                        trains.trains[i].direction = self.tiles[self.front_y][self.front_x].attached.d180
                    elif trains.trains[i].degree == 270:
                        trains.trains[i].direction = self.tiles[self.front_y][self.front_x].attached.d270

    def create_point(self):
        # randomly generate 2 set of coordinate from (0, 0) to (NUM_COLS - 1, NUM_ROWS - 1)
        '''
        self.distance = 0
        self.i = 0
        while self.distance < 5:
            self.start = (random.randint(0, NUM_COLS - 1 - self.i), random.randint(0 + self.i, NUM_ROWS - 1))
            self.end = (random.randint(0, NUM_COLS - 1 - self.i), random.randint(0 + self.i, NUM_ROWS - 1))
            self.i += 1
            if self.i > NUM_COLS - 1:
                self.i = NUM_COLS - 1
            self.distance = math.sqrt((self.end[0] - self.start[0])**2 + (self.end[1] - self.start[1])**2)
        '''
        # determine orientation for locations
        self.start = (0, 0)
        self.end = (0, 9)

        # starting location
        image = TrackSprites.train_station
        point_rect = pygame.Rect(self.rect.left + OUTER_GAP + self.start[0] * (TRACK_WIDTH + INNER_GAP), self.rect.top + OUTER_GAP + self.start[1] * (TRACK_HEIGHT + INNER_GAP) , TRACK_WIDTH, TRACK_HEIGHT)
        #self.data = {"point": "start", "orient": self.train_orient(self.start), "set": self.total_paths}

        start_station = Station(
            type = "station",
            image = image, 
            rect = point_rect, 
            point = 'start', 
            orientation = 270, 
            id = self.total_paths
        )
        self.tiles[self.start[1]][self.start[0]].attached = start_station

        
        # ending location
        point_rect = pygame.Rect(self.rect.left + OUTER_GAP + self.end[0] * (TRACK_WIDTH + INNER_GAP), self.rect.top + OUTER_GAP + self.end[1] * (TRACK_HEIGHT + INNER_GAP) , TRACK_WIDTH, TRACK_HEIGHT)
        end_station = Station(
            type = "station",
            image = image, 
            rect = point_rect, 
            point = 'end', 
            orientation = 90, 
            id = self.total_paths
        )
        self.tiles[self.end[1]][self.end[0]].attached = end_station
        
        # spawn_train(degree, speed, x, y, direction)
        # direction could be "forward", "clockwise", or "counter-clockwise"

        # print(self.tiles[self.start[1]][self.start[0]].attached.data)
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
        if location[0] == 9:
            self.orient.remove(0)

        if location[1] == 0:
            self.orient.remove(90)
        if location[1] == 9:
            self.orient.remove(270)

        return self.orient[random.randint(0, len(self.orient) - 1)]

    '''
    def create_new_path(self):
        # Find needed variables
        path_index = len(self.tile_paths)
        sides = ['top', 'bottom', 'left', 'right']

        # Helper functions
        def find_random_tile_on_side(side):
            max_row = NUM_ROWS - 1
            max_col = NUM_COLS - 1
            index = random.randint(3, max_col - 1)
            if side == 'left' or side == 'right': index = random.randint(3, max_row - 1)

            if side == 'top': return self.tiles[0][index]
            if side == 'bottom': return self.tiles[max_row][index]
            if side == 'left': return self.tiles[index][0]
            if side == 'right': return self.tiles[index][max_col]
        def find_unused_path_tile(side, path_index):
            for i in range(200): # Ardbitrary range to end if fail
                tile = find_random_tile_on_side(side)
                if tile.try_set_tile_to_path(path_index): return tile
            return None

        # Finds 2 tiles for the path
        tiles_in_path = []
        for i in range(2):
            side = random.choice(sides)
            tile = find_unused_path_tile(side, path_index)
            tiles_in_path.append(tile)
            sides.remove(side)

        if None in tiles_in_path: return
        self.tile_paths.append(tiles_in_path)
    '''
    
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

    '''
    def draw_path_tiles(self, game_surf):
        for path in self.tile_paths:
            for tile in path:
                pygame.draw.rect(game_surf, Colors.red, tile.rect)
    '''