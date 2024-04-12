import random
from constants import *
from track_set import TrackSet
from track_set_types import SpawnTracks, TrackSetTypes

class TrackSetSpawner:
    def __init__(self, rect):
        self.rect = rect
        self.item = None

    # Spawner logic
    def spawn_track_set(self):
        if self.item: return None

        set_type = random.choice(SpawnTracks)
        track_set = TrackSet(
            pos = self.rect.topleft,
            type = set_type
        )
        track_set.set_position_by_center(self.rect.center)
        
        self.item = track_set
        return track_set



    # Rendering
    def draw(self, game_surf):
        pygame.draw.rect(game_surf, Colors.black, self.rect)
