# The board holding and controlling the tiles

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
    
    def find_tile_in_location(self, pos):
        x, y = pos

        row = ((y - self.rect.top - OUTER_GAP) - NUM_ROWS * ((y - self.rect.top - OUTER_GAP) // 55)) // 50
        col = ((x - self.rect.left - OUTER_GAP) - NUM_COLS * ((x - self.rect.left - OUTER_GAP) // 55)) // 50

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
        self.draw_tracks(game_surf)

    def draw_board(self, game_surf):
        pygame.draw.rect(game_surf, Colors.light_gray, self.rect)
    def draw_tiles(self, game_surf):
        for row in self.tiles:
            for tile in row:
                pygame.draw.rect(game_surf, Colors.white, tile.rect)
    def draw_tracks(self, game_surf):
        for row in self.tiles:
            for tile in row:
                if tile.attached_track is not None:
                    scaled_image_grid = pygame.transform.scale(tile.attached_track.image, (TRACK_WIDTH, TRACK_HEIGHT))
                    center = tile.attached_track.rect.move(0, 0)
                    game_surf.blit(scaled_image_grid, center)