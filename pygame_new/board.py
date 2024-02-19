# Handles logic of the game board and tiles

import pygame
from constants import *
from tile import Tile

class Board:
    def __init__(self):
        board_width = NUM_COLS * TRACK_WIDTH + INNER_GAP * (NUM_COLS - 1) + OUTER_GAP * 2
        board_height = NUM_ROWS * TRACK_HEIGHT + INNER_GAP * (NUM_ROWS - 1) + OUTER_GAP * 2
        board_x = GAME_WIDTH / 2 - board_width / 2
        board_y = GAME_HEIGHT * 0.1
        self.rect = pygame.Rect(board_x, board_y, board_width, board_height)
        self.tiles = self.create_grid()

        # Create track box
        track_box_width = 5 * TRACK_WIDTH + (TRACK_SEPERATION - TRACK_WIDTH) * (5 - 1) + EXTRA_WIDTH * 4
        track_box_height = TRACK_HEIGHT + EXTRA_HEIGHT * 2
        track_box_x = GAME_WIDTH / 2 - track_box_width / 2
        track_box_y = GAME_HEIGHT * 0.85
        self.track_box = pygame.Rect(track_box_x, track_box_y, track_box_width, track_box_height)

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

    # def update_tracks_in_grid(self, tracks):
    #     for i, row in enumerate(self.tiles):
    #         for j, tile in enumerate(row):
    #             if tile.attached_track in tracks:
    #                 continue
    #             tile.attached_track = None

    def draw_board(self, game_surf):
        pygame.draw.rect(game_surf, Colors.light_gray, self.rect)
        for row in self.tiles:
            for tile in row:
                pygame.draw.rect(game_surf, Colors.white, tile.rect)

    def draw_tracks_on_board(self, game_surf):
        for row in self.tiles:
            for tile in row:
                if tile.attached_track is not None:
                    scaled_image_grid = pygame.transform.scale(tile.attached_track.image, (TRACK_WIDTH, TRACK_HEIGHT))
                    center = tile.attached_track.rect.move(0, 0)
                    game_surf.blit(scaled_image_grid, center)

    def draw_track_box(self, game_surf, tracks):
        pygame.draw.rect(game_surf, Colors.black, self.track_box)

        for track in tracks:
            scaled_image = pygame.transform.scale(track.image, (TRACK_WIDTH, TRACK_HEIGHT))
            game_surf.blit(scaled_image, track.rect)