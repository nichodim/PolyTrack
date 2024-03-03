import random
from constants import *
from track_set import TrackSet
from track_set_types import SpawnTracks, TrackSetTypes

class TrackSetSpawner:
    def __init__(self, rect):
        self.rect = rect
        self.item = None

    # Spawner logic
    def track_set_over_box(self, track_set):
        positions = track_set.find_pos_of_tracks()
        for pos in positions:
            track_in_box = self.rect.collidepoint(pos)
            if not track_in_box: return False
        return True

    def find_valid_track_set(self, set_type):
        x_range = self.rect.right - self.rect.left
        y_range = self.rect.bottom - self.rect.top

        valid_location = False
        while not valid_location:
            offsetx, offsety = random.randrange(x_range), random.randrange(y_range)
            
            x = self.rect.left + offsetx
            y = self.rect.top + offsety
            
            track_set = TrackSet(
                pos = (x, y), 
                type = set_type
            )
            valid_location = self.track_set_over_box(track_set)

        return track_set

    def spawn_track_set(self):
        if self.item: return None

        set_type = random.choice(SpawnTracks)
        track_set = self.find_valid_track_set(set_type)
        
        self.item = track_set
        return track_set



    # Rendering
    def draw(self, game_surf):
        pygame.draw.rect(game_surf, Colors.black, self.rect)
