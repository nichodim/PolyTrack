# The board holding and controlling the tiles
import random
import pygame
from constants import *
from tile import Tile
from obstacle import Obstacle
from path import Path

class Board:
    def __init__(self, end_call):
        # Create board
        self.rect = pygame.Rect(board_x, board_y, board_width, board_height)

        # Create tiles
        self.tiles = self.create_grid()
        self.generate_obstacles(random.randint(2, 6))
        self.highlighted_tiles = []

        self.end_call = end_call
        self.paths = []

        self.create_path()


    # Board Creation
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
    
    def create_path(self):
        new_path = Path(
            board_tiles = self.tiles, 
            board_rect = self.rect, 
            end_call = self.path_call
        )
        self.paths.append(new_path)
    

    # Extra Board Logic
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
            0 <= row <= NUM_ROWS - 1 and # valid row
            0 <= col <= NUM_COLS - 1 and # valid column
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

        if len(self.paths) < 1:
            self.create_path()
    
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
                r, g, b = Colors.green
                highlight_surf.fill((r,g,b,128))
                game_surf.blit(highlight_surf, tile.rect.topleft)
    
    def draw_paths(self, game_surf):
        for path in self.paths:
            path.draw(game_surf)