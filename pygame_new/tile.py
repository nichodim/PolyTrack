# Handles tiles

from track import Track

class Tile:
    def __init__(self, rect):
        self.rect = rect
        self.attached_track = None
    
    def update_attached_track(self, Track):
        if self.attached_track != None:
            return False
        self.attached_track = Track
        return True
