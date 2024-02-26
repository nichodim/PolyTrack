# The board holding and controlling the tiles
import random
import pygame
from constants import *
from tile import Tile

class Board:
    def __init__(self):
        # Create board
        board_width = NUM_COLS * TRACK_WIDTH + INNER_GAP * (NUM_COLS - 1) + OUTER_GAP * 2
        board_height = NUM_ROWS * TRACK_HEIGHT + INNER_GAP * (NUM_ROWS - 1) + OUTER_GAP * 2
        board_x = GAME_WIDTH / 2 - board_width / 2
        board_y = GAME_HEIGHT * 0.1
        self.rect = pygame.Rect(board_x, board_y, board_width, board_height)

        # Create tiles
        self.tiles = self.create_grid()

        # Create tile paths - TODO creation should be an event
        self.tile_paths = []
        self.create_new_path()


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
            for i in range(200):
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

    
    # TODO calculation does not work on grids that arent 10 by 10
    def find_tile_in_location(self, pos):
        x, y = pos

        y_no_margin = y - self.rect.top - OUTER_GAP
        row = int((y_no_margin - INNER_GAP * (y_no_margin // (TRACK_HEIGHT + INNER_GAP))) // TRACK_HEIGHT)
        
        x_no_margin = x - self.rect.left - OUTER_GAP
        col = int((x_no_margin - INNER_GAP * (x_no_margin // (TRACK_WIDTH + INNER_GAP))) // TRACK_WIDTH)
        print('row:', row, '-', 'col:', col)

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
        self.draw_path_tiles(game_surf)
        self.draw_tracks(game_surf)
        
    def draw_board(self, game_surf):
        pygame.draw.rect(game_surf, Colors.light_gray, self.rect)
    def draw_tiles(self, game_surf):
        for row in self.tiles:
            for tile in row:
                pygame.draw.rect(game_surf, Colors.white, tile.rect)
    
    def draw_path_tiles(self, game_surf):
        for path in self.tile_paths:
            for tile in path:
                pygame.draw.rect(game_surf, Colors.red, tile.rect)

    def draw_tracks(self, game_surf):
        for row in self.tiles:
            for tile in row:
                if tile.attached_track is not None:
                    scaled_image_grid = pygame.transform.scale(tile.attached_track.image, (TRACK_WIDTH, TRACK_HEIGHT))
                    center = tile.attached_track.rect.move(0, 0)
                    game_surf.blit(scaled_image_grid, center)