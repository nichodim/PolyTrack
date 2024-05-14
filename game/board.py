# The board holding and controlling the tiles
import random
import pygame

from itertools import product
from constants import *
from tile import Tile
from obstacle import Obstacle
from path import Path
from weather import Weather
from timer import Timer

class Board:
    def __init__(self, map, end_call, complete_map, animate_weather):
        self.clocks = []
        # Find custom map values
        grid_layout = map['board']
        self.type, self.obstacles, self.levels = map['type'], map['obstacles'], map['levels']
        self.rows, self.cols = len(grid_layout), len(grid_layout[0])
        self.end_call, self.complete_map, self.animate_weather = end_call, complete_map, animate_weather
        
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

        # Create highlighting for tiles
        self.highlighted_tiles = []
        self.highlight_color = Colors.green
        self.default_highlight_opacity = 128

        # Create highlighting for board
        self.board_highlight_rect = pygame.Rect(board_x - 10, board_y - 10, board_width + 2*10, board_height + 2*10)
        self.highlight_state_config = {
            'freeze': [Colors.blue, 128], 
            'freeze-hover': [Colors.blue, 64]
        }
        self.board_highlight = False

        # Creatre path boilerplate
        self.paths = []

        # Load explosion images
        self.explosion_images = PowerupSprites.explosion_images
        self.explosion_index = 0
        self.explosion_rect = pygame.Rect(0, 0, 0, 0)
        self.explosion_animation_speed = 40

        # Start levels
        self.level, self.round = 0, 0
        self.new_level()

        self.animate = False
        self.animate_duration = 0

        self.i = 0

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
    
    # Modified By Kelvin Huang, May 12, 2024
    # split previous new_round function to new_level and new_round to handle weather
    def new_level(self):
        # clear board
        for row in self.tiles:
            for tile in row:
                tile.attached = None
                if self.type == 'frozen' and tile.terrain == 'water':
                    tile.terrain = 'ice'
        
        # Generate new obstacles
        obstacle_range = self.levels[self.level]['obstacle_range']
        self.generate_obstacles(obstacle_range)
        
        # add first set of train
        trains_to_spawn = self.levels[self.level]['rounds'][self.round]
        for train_type in trains_to_spawn:
            self.create_path(train_type)
    
    def new_round(self):
        self.round += 1

        # Check level, if done all rounds (or first)...
        if len(self.levels[self.level]['rounds']) <= self.round: 
            # Go to next level
            self.level += 1
            self.round = 0

            # Check if done all levels
            if len(self.levels) <= self.level: self.complete_map()

            # start animation between board clearing
            self.animate = True
            self.animate_duration = 3 * 60 
            self.animate_weather("hail")
            return # prevent next train from being added
            
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
            grid_dimensions = (self.rows, self.cols),
            add_clock = self.add_clock,                 # Modified by Kelvin Huang, May 13, 2024
            tick_clock = self.tick_clock                # pass these method to path so it can use it to add timer above starting stations  
        )
        self.paths.append(new_path)
    
    # Path has returned end condition
    # End condition is then passed up to board
    # Be careful with update and deletion, can cause crashing
    def path_call(self, path, condition):
        path.remove_all_under() # added by Kelvin Huang, April 28, 2024 delete all reference to path
        self.paths.remove(path)
        del path

        # Tell the game that the board has end condition
        self.end_call(condition)

        if len(self.paths) == 0: self.new_round()

    def toggle_fast_forward(self, active):
        for path in self.paths:
            path.toggle_speed_multiplier('fast_forward', active)

    # Extra Board Logic
    def get_tiles_in_radius(self, radius, tile):
        row, col = self.tile_indexes[f'{tile}']
        tiles = [tile]

        # Circle bomb blast
        def spread_coords(coord, r):
            # Modified By Kelvin Huang, 4/18/2024
            # Fixed issue where large board crash on the last row
            x, y = coord
            if 0 <= x+1 < self.rows: 
                tiles.append(self.tiles[x+1][y])
                if r < radius: spread_coords((x+1, y), r+1)
            if 0 <= x-1 < self.rows: 
                tiles.append(self.tiles[x-1][y])
                if r < radius: spread_coords((x-1, y), r+1)
            if 0 <= y+1 < self.cols: 
                tiles.append(self.tiles[x][y+1])
                if r < radius: spread_coords((x, y+1), r+1)
            if 0 <= y-1 < self.cols: 
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
    
    def activate_freeze(self, paths):
        for path in self.paths:
            if path in paths: 
                path.toggle_speed_multiplier('freeze', True)
                path.powerup_time = 0

                path.highlight = 'freeze'
                path.prev_highlight = ''
    
    def trigger_powerup(self, powerup, tile_under, game_surf):
        def trigger_bomb():
            # Start explosion animation
            new_center = (tile_under.rect.center[0], tile_under.rect.center[1])
            self.animate_explosion(new_center, game_surf)

            for tile in self.highlighted_tiles:
                if tile.terrain == 'ice': tile.terrain = 'water'

                everything_effected = len(powerup.type['effected attachments']) == 0
                is_effected = tile.attached.__class__.__name__ in powerup.type['effected attachments']
                if everything_effected or is_effected:
                    tile.attached = None

                # Modified by Kelvin Huang, April 28, 2024
                # destroy path if train is on top of the tile bomb
                
                # Modified by Kelvin Huang, April 29, 2024
                # adjust code to work with multiple cart
                # if path get delete once there is no need to delete it again
                delete_path = False
                if tile.under_path != None and not delete_path:
                    tile.under_path.delete(False)
                    delete_path = True
            self.unhighlight()
        
        def trigger_freeze():
            everything_effected = len(powerup.type['effected attachments']) == 0
            if everything_effected: 
                if tile_under.under_path != None: self.activate_freeze([tile_under.under_path])
                else: self.activate_freeze(self.paths)

        if powerup.type_name == 'bomb' or powerup.type_name == 'bigbomb':
            trigger_bomb()
        
        if powerup.type_name == 'freeze':
            trigger_freeze()

    def animate_explosion(self, position, game_surf):
        for image in self.explosion_images:
            self.explosion_rect = image.get_rect(center=position)

            game_surf.blit(image, self.explosion_rect)
            pygame.display.flip()

            pygame.time.delay(self.explosion_animation_speed)

        self.explosion_index = 0

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
    
    def add_clock(self, x, y, radius, duration):    # Created by Kelvin Huang, May 13, 2024 
        clock = Timer(x, y, radius, duration)       # handles adding new clock in board.py
        self.clocks.append(clock)        
        return clock
    
    def tick_clock(self, clock, speed = 1):         # handles ticking new clock in board.py
        if clock.tick(speed) == True:
            self.clocks.remove(clock)
            return True

    def update(self):
        # for train
        if self.animate == True:
            self.animate_duration -= 1
            if self.animate_duration == 0: 
                self.animate = False
                self.new_level()
                
        else:
            for path in self.paths:
                path.update()

    # Rendering
    def draw(self, game_surf):
        self.draw_board(game_surf)
        self.draw_tiles(game_surf)
        self.draw_paths(game_surf)
        self.draw_board_highlight(game_surf)
        self.draw_clocks(game_surf)
        
    def get_highlight_box(self, width, height, color, opacity):
        highlight_surf = pygame.Surface((width,height), pygame.SRCALPHA)
        r, g, b = color
        highlight_surf.fill((r,g,b,opacity))
        return highlight_surf

    def draw_board(self, game_surf):
        pygame.draw.rect(game_surf, Colors.light_gray, self.rect)

    def draw_highlight(self, tile, game_surf):
        if not tile.highlighted: return
        game_surf.blit(self.get_highlight_box(
            TRACK_WIDTH, TRACK_HEIGHT, self.highlight_color, self.default_highlight_opacity
        ), tile.rect.topleft)

    def draw_tiles(self, game_surf):
        for row in self.tiles:
            for tile in row:
                tile.draw_attached(game_surf)
                self.draw_highlight(tile, game_surf)
    
    def draw_paths(self, game_surf):
        for path in self.paths:
            path.draw(game_surf)

            # Rerender highlight for station tiles
            rerendered_tiles = [path.start_station_tile, path.end_station_tile]
            for tile in rerendered_tiles:
                self.draw_highlight(tile, game_surf)
    
    def draw_board_highlight(self, game_surf):
        if len(self.paths) == 0: return
        all_highlighted = True
        all_highlightes_as = self.paths[0].highlight
        for path in self.paths:
            if path.highlight == '' or path.highlight != all_highlightes_as:
                all_highlighted = False
                break
        
        if all_highlighted:
            color, opacity = self.highlight_state_config[all_highlightes_as]
            game_surf.blit(self.get_highlight_box(
                self.board_highlight_rect.width, self.board_highlight_rect.height, color, opacity
            ), self.board_highlight_rect.topleft)
        else:
            for path in self.paths:
                if path.highlight != '':
                    if all_highlighted: 
                        if 'hover' not in path.highlight: continue
                    
                    color, opacity = self.highlight_state_config[path.highlight]
                    for (col, row) in path.tiles_under:
                        tile = self.tiles[row][col]
                        game_surf.blit(self.get_highlight_box(
                            tile.rect.width, tile.rect.height, color, opacity
                        ), tile.rect.topleft)
    
    def draw_clocks(self, game_surf):       # Created by Kelvin Huang, May 13, 2024
        for clock in self.clocks:           # Draw each clock
            clock.draw(game_surf)