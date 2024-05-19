# Handles tiles

from constants import *
from board_item_types import TerrainTypes

class Tile:
    def __init__(self, rect, terrain = 'grass'):
        self.rect = rect
        self.terrain = terrain
        self.attached = None
        self.highlighted = False
        self.under_path = None
        self.slowed = False
    
    def is_open(self):
        return not self.attached and self.terrain != 'water'

    def attach(self, item):
        if self.is_open():
            self.attached = item
            return True
        return False

    def draw_attached(self, game_surf):
        scaled_image_grid = pygame.transform.scale(TerrainTypes[self.terrain], (TRACK_WIDTH, TRACK_HEIGHT))
        game_surf.blit(scaled_image_grid, self.rect.topleft)

        if self.attached:
            scaled_image_grid = pygame.transform.scale(self.attached.image, (TRACK_WIDTH, TRACK_HEIGHT))
            game_surf.blit(scaled_image_grid, self.rect.topleft)
    
    def draw_effect(self, game_surf):
        if self.slowed:
            game_surf.blit(get_highlight_box(
                    self.rect.width, self.rect.height, (255, 255, 0)
                ), self.rect.topleft)

class TimedTileEffect:
    def __init__(self, tiles, time_limit, action, undo):
        self.tiles = tiles
        self.undo = undo
        for tile in tiles:
            action(tile)

        self.time_limit = time_limit
        self.time = 0
        self.done = False

    def remove_tiles(self, tiles, undo_effect = False):
        for tile in tiles:
            if tile in self.tiles:
                self.tiles.remove(tile)
                if undo_effect: self.undo(tile)
    
    def update(self):
        self.time += 1
        if self.time >= self.time_limit:
            self.done = True
    
    def __del__(self):
        for tile in self.tiles:
            self.undo(tile)
        del self