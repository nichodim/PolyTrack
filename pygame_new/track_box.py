# The box holding and controlling the tracks - once tracks are placed on the board, tracks are no longer considered tracks

import random
from constants import *
from track_set import TrackSet
from track_set_types import TrackSetTypes

class Trackbox:
    def __init__(self):
        # Create track box
        track_box_width = 5 * TRACK_WIDTH + (TRACK_SEPERATION - TRACK_WIDTH) * (5 - 1) + EXTRA_WIDTH * 4
        track_box_height = TRACK_HEIGHT + EXTRA_HEIGHT * 2
        track_box_x = GAME_WIDTH / 2 - track_box_width / 2
        track_box_y = GAME_HEIGHT * 0.85
        self.rect = pygame.Rect(track_box_x, track_box_y, track_box_width, track_box_height)

        # Create tracks
        self.track_sets = []


    # Track box game logic
    def generate_new_track_sets(self):  
        not_enough_sets = len(self.track_sets) < 5
        if not_enough_sets:
            set_name = random.choice(list(TrackSetTypes))
            set_type = TrackSetTypes[set_name]
            x = self.rect.left + EXTRA_WIDTH * 2 + TRACK_SEPERATION * len(self.track_sets)
            y = self.rect.centery - EXTRA_HEIGHT

            track_set = TrackSet(
                pos = (x, y), 
                type = set_type
            )
            self.track_sets.append(track_set)

    def find_track_set(self, pos):
        for set in self.track_sets:
            if set.is_in_pos(pos): return set
        return None
    
    def remove_track_set(self, track_set):
        i = self.track_sets.index(track_set)
        self.track_sets.remove(track_set)
        for j in range(i, len(self.track_sets)):
            track_set = self.track_sets[j]
            track_set.move((-TRACK_SEPERATION, 0))

    def track_set_to_initial(self, track_set):
        i = self.track_sets.index(track_set)
        x = self.rect.left + EXTRA_WIDTH * 2 + TRACK_SEPERATION * i
        y = self.rect.centery - EXTRA_HEIGHT
        track_set.set_position((x, y))

    def update(self):
        self.generate_new_track_sets()


    # Rendering
    def draw(self, game_surf):
        self.draw_track_box(game_surf)
        self.draw_track_sets(game_surf)

    def draw_track_box(self, game_surf):
        pygame.draw.rect(game_surf, Colors.black, self.rect)
    def draw_track_sets(self, game_surf):
        for track_set in self.track_sets:
            track_set.draw(game_surf)