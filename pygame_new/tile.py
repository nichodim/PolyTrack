# Handles tiles

from track import Track

class Tile:
    def __init__(self, rect):
        self.rect = rect
        self.attached_track = None
    
    def try_attach_track(self, track):
        if self.attached_track:
            return False
        self.attached_track = track
        return True
