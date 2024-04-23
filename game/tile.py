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
    
    def is_open(self):
        return not self.attached

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