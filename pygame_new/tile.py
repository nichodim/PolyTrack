# Handles tiles

from constants import *

class Tile:
    def __init__(self, rect):
        self.rect = rect
        self.attached = None
        self.highlighted = False
    
    def is_open(self):
        return not self.attached

    def attach(self, item):
        if self.is_open():
            self.attached = item
            return True
        return False

    '''
    def try_set_tile_to_path(self, i):
        if self.in_path >= 0:
            return False
        self.in_path = i
        return True
    '''

    def draw_attached(self, game_surf):
        if self.attached:
            scaled_image_grid = pygame.transform.scale(self.attached.image, (TRACK_WIDTH, TRACK_HEIGHT))
            game_surf.blit(scaled_image_grid, self.rect.topleft)