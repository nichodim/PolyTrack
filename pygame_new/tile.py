# Handles tiles

from track import Track

class Tile:
    def __init__(self, rect):
        self.rect = rect
        self.attached_track = None
        self.in_path = -1
    
    def try_attach_track(self, track):
        if self.attached_track:
            return False
        self.attached_track = track
        return True
    
    def try_set_tile_to_path(self, i):
        if self.in_path >= 0:
            return False
        self.in_path = i
        return True
