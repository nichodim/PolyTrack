# The board holding and controlling the tiles
import random
import pygame
from itertools import product
from constants import *
from tile import Tile
from obstacle import Obstacle
from path import Path

class Board:
    def __init__(self, map, end_call, complete_map):
        # Find custom map values
        grid_layout = map['board']
        self.type, self.obstacles, self.levels = map['type'], map['obstacles'], map['levels']
        self.rows, self.cols = len(grid_layout), len(grid_layout[0])
        self.end_call, self.complete_map = end_call, complete_map

        # Create board
        board_width = self.cols * TRACK_WIDTH + INNER_GAP * (self.cols - 1) + OUTER_GAP * 2
        board_height = self.rows * TRACK_HEIGHT + INNER_GAP * (self.rows - 1) + OUTER_GAP * 2
        board_x = GAME_WIDTH / 2 - board_width / 2
        board_y = GAME_HEIGHT * 0.05
        self.rect = pygame.Rect(board_x, board_y, board_width, board_height)

        # Create tiles
        self.tiles = self.create_grid(grid_layout)
        self.tile_indexes = {}
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                self.tile_indexes[f'{tile}'] = (i, j)

        self.highlighted_tiles = []
        self.highlight_color = Colors.red
        self.paths = []

        # Start levels
        self.level, self.round = -1, -1
        self.new_round()

    def set_f_pressed(self, value):
        self.f_pressed = value
    
    def update_path_f_pressed(self, value):
        for path in self.paths:
            path.set_f_pressed(value)

    # Board Creation
    def create_grid(self, grid_layout):
        tiles = []
        row_y_increment = TRACK_HEIGHT + INNER_GAP
        row_y = self.rect.top + OUTER_GAP

        for row in grid_layout:
            tile_x = OUTER_GAP
            row_list = []
            
            for col in row:
                tile_rect = pygame.Rect(self.rect.left + tile_x, row_y, TRACK_WIDTH, TRACK_HEIGHT)
                row_list.append(Tile(tile_rect, col))
                tile_x += TRACK_WIDTH + INNER_GAP

            tiles.append(row_list)
            row_y += row_y_increment

        return tiles
    
    def new_round(self):
        self.round += 1

        # Check level, if done all rounds (or first)...
        if self.level == -1 or len(self.levels[self.level]['rounds']) <= self.round: 
            # Go to next level
            self.level += 1
            self.round = 0

            # Check if done all levels
            if len(self.levels) <= self.level: self.complete_map()

            # Reset board
            for row in self.tiles:
                for tile in row:
                    tile.attached = None
            
            # Generate new obstacles
            obstacle_range = self.levels[self.level]['obstacle_range']
            self.generate_obstacles(obstacle_range)
        
        # Add new trains
        trains_to_spawn = self.levels[self.level]['rounds'][self.round]
        for train_type in trains_to_spawn:
            self.create_path(train_type)

    def generate_obstacles(self, possible_range):
        a, b = possible_range
        num = random.randint(a, b)
        for n in range(num):
            for m in range(100):
                row = random.randrange(self.rows)
                col = random.randrange(self.cols)
                tile = self.tiles[row][col]

                attached = tile.attach(Obstacle(self.obstacles))
                if attached: break
    
    def create_path(self, train_type):
        new_path = Path(
            board_tiles = self.tiles, 
            board_rect = self.rect, 
            end_call = self.path_call, 
            train_type = train_type,
            grid_dimensions = (self.rows, self.cols)
        )
        self.paths.append(new_path)
    

    # Extra Board Logic
    def get_tiles_in_radius(self, radius, tile):
        row, col = self.tile_indexes[f'{tile}']
        tiles = [tile]

        # Circle bomb blast
        def spread_coords(coord, r):
            x, y = coord
            if 0 <= x+1 < self.cols: 
                tiles.append(self.tiles[x+1][y])
                if r < radius: spread_coords((x+1, y), r+1)
            if 0 <= x-1 < self.cols: 
                tiles.append(self.tiles[x-1][y])
                if r < radius: spread_coords((x-1, y), r+1)
            if 0 <= y+1 < self.rows: 
                tiles.append(self.tiles[x][y+1])
                if r < radius: spread_coords((x, y+1), r+1)
            if 0 <= y-1 < self.rows: 
                tiles.append(self.tiles[x][y-1])
                if r < radius: spread_coords((x, y-1), r+1)
        
        spread_coords((row, col), 1)
        return tiles

        # Square bomb blast
        # radius_squared = radius ** 2
        # for x, y in product(range(-radius, radius + 1), repeat=2):
        #     if x ** 2 + y ** 2 < radius_squared:
        #         tile_x, tile_y = x + row, y + col
        #         if 0 <= tile_x < self.cols and 0 <= tile_y < self.rows:
        #             tiles.append(self.tiles[tile_x][tile_y])
        # return tiles
    
    def highlight_bomb_tiles(self, powerup, tile):
        tiles_to_highlight = self.get_tiles_in_radius(powerup.type['blast radius'], tile)
        self.highlight(tiles_to_highlight)
    
    def trigger_powerup(self, powerup, tile):
        if powerup.type_name == 'bomb':
            print('bomb activated!')
            for tile in self.highlighted_tiles:
                tile.attached = None

            self.unhighlight()

    def unhighlight(self):
        for tile in self.highlighted_tiles:
            tile.highlighted = False
        self.highlighted_tiles = []
    def highlight(self, tiles):
        self.unhighlight()

        for tile in tiles:
            tile.highlighted = True
            self.highlighted_tiles.append(tile)

    def find_tile_in_location(self, pos):
        x, y = pos

        y_no_margin = y - self.rect.top - OUTER_GAP
        row = int((y_no_margin - INNER_GAP * (y_no_margin // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
        
        x_no_margin = x - self.rect.left - OUTER_GAP
        col = int((x_no_margin - INNER_GAP * (x_no_margin // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)

        if ( 
            0 <= row <= self.rows - 1 and # valid row
            0 <= col <= self.cols - 1 and # valid column
            self.tiles[row][col].rect.collidepoint(pos) # over tile
        ):
            return self.tiles[row][col]
        return None
    
    # Path has returned end condition
    # End condition is then passed up to board
    # Be careful with update and deletion, can cause crashing
    def path_call(self, path, condition):
        self.paths.remove(path)
        del path

        # Tell the game that the board has end condition
        self.end_call(condition)

        if len(self.paths) == 0: self.new_round()
    
    def update(self):
        # for trian
        for path in self.paths:
            path.update()


    # Rendering
    def draw(self, game_surf):
        self.draw_board(game_surf)
        self.draw_tiles(game_surf)
        self.draw_paths(game_surf)
        
    def draw_board(self, game_surf):
        pygame.draw.rect(game_surf, Colors.light_gray, self.rect)

    def draw_tiles(self, game_surf):
        for row in self.tiles:
            for tile in row:
                tile.draw_attached(game_surf)
                if not tile.highlighted: continue

                highlight_surf = pygame.Surface((TRACK_WIDTH,TRACK_HEIGHT), pygame.SRCALPHA)
                r, g, b = self.highlight_color
                highlight_surf.fill((r,g,b,128))
                game_surf.blit(highlight_surf, tile.rect.topleft)
    
    def draw_paths(self, game_surf):
        for path in self.paths:
            path.draw(game_surf)