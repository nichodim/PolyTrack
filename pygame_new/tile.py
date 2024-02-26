# Handles tiles

class Tile:
    def __init__(self, rect):
        self.rect = rect
        self.attached_track = None
        self.in_path = -1
    
    def is_open(self):
        return not self.attached_track

    def attach_track(self, track):
        if self.is_open():
            self.attached_track = track
            return True
        return False
    
    def try_set_tile_to_path(self, i):
        if self.in_path >= 0:
            return False
        self.in_path = i
        return True