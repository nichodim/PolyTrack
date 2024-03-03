# The box holding and controlling the tracks - once tracks are placed on the board, tracks are no longer considered tracks

import random
from constants import *
from button_toggle import ButtonToggle
from track_set_spawner import TrackSetSpawner
from track_set import TrackSet
from track_set_types import SpawnTracks, TrackSetTypes

class Trackbox:
    def __init__(self):
        # Create track box
        track_box_width = 7 * TRACK_WIDTH + (TRACK_SEPERATION - TRACK_WIDTH) * (5 - 1) + EXTRA_WIDTH * 4
        track_box_height = TRACK_HEIGHT * 3 + EXTRA_HEIGHT * 2
        track_box_x = GAME_WIDTH / 2 - track_box_width / 2
        track_box_y = GAME_HEIGHT * 0.725
        self.rect = pygame.Rect(track_box_x, track_box_y, track_box_width, track_box_height)

        # Create track set spawner
        spawner_width = TRACK_WIDTH * 3
        spawner_height = TRACK_HEIGHT * 3
        spawner_x = self.rect.right - spawner_width - EXTRA_WIDTH / 2
        spawner_y = self.rect.top + EXTRA_HEIGHT
        spawner_rect = pygame.Rect(spawner_x, spawner_y, spawner_width, spawner_height)
        self.spawner = TrackSetSpawner(spawner_rect)
        self.spawner_button = ButtonToggle(self.spawner.rect, (Colors.green, Colors.red))

        # Create tracks
        self.track_sets = []


    # Track box game logic
    def generate_track_set(self):  
        track_set = self.spawner.spawn_track_set()
        self.track_sets.append(track_set)

    def track_set_over_box(self, track_set):
        positions = track_set.find_pos_of_tracks()
        for pos in positions:
            track_in_box = self.rect.collidepoint(pos)
            if not track_in_box: return False
        return True
    def find_precise_pos_of_tracks(self):
        positions = []
        for track in self.tracks:
            pos = ((track.rect.left, track.rect.top), (track.rect.right, track.rect.bottom))
            positions.append(pos)
        return positions

    def find_track_set(self, pos):
        for track_set in self.track_sets:
            if track_set.is_in_pos(pos): return track_set
        return None

    def find_hovered_track_and_index(self, track_set):
        mouse_pos = pygame.mouse.get_pos()
        hovered_track = track_set.find_track_in_pos(mouse_pos)
        hovered_track_index = track_set.tracks.index(hovered_track)
        return (hovered_track, hovered_track_index)
    
    def remove_track_set(self, track_set):
        i = self.track_sets.index(track_set)
        self.track_sets.remove(track_set)
        for j in range(i, len(self.track_sets)):
            track_set = self.track_sets[j]
            track_set.move((-TRACK_SEPERATION, 0))

    # Increments given set type by 1 or resets to first if looped around
    def increment_type(self, set_type):
        type_keys = list(TrackSetTypes.keys())
        types = list(TrackSetTypes.values())
        type_key = type_keys[types.index(set_type)]
        key_num = int(type_key[-1:])

        new_key_num = key_num + 1
        new_key = type_key[:-1] + str(new_key_num)

        if not new_key in type_keys: new_key = type_key[:-1] + '1'
        return TrackSetTypes[new_key]
    
    # Rotates the track set by replacing it with the incremented type in type_sets
    def rotate(self, track_set, hovered_track_and_index):
        hovered_track, hovered_index = hovered_track_and_index
        new_type = self.increment_type(track_set.structure)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_pos = (mouse_x - TRACK_WIDTH // 2, mouse_y - TRACK_HEIGHT // 2)

        # Sets position of tracks based on the track that was under the mouse previously
        new_set = TrackSet((0, 0), new_type)
        new_set.set_position(new_pos, hovered_index)

        set_index = self.track_sets.index(track_set)
        self.track_sets[set_index] = new_set
        return new_set

    def handle_spawn_button(self):
        if self.spawner_button.clicked():
            self.generate_track_set()
    def update_spawner(self, track_set):
        if track_set != self.spawner.item: return
        self.spawner.item = None
        self.spawner_button.untoggle()


    # Rendering
    def draw(self, game_surf):
        self.draw_track_box(game_surf)
        self.spawner.draw(game_surf)
        self.spawner_button.draw(game_surf)
        self.draw_track_sets(game_surf)

    def draw_track_box(self, game_surf):
        pygame.draw.rect(game_surf, Colors.black, self.rect)
    def draw_track_sets(self, game_surf):
        for track_set in self.track_sets:
            track_set.draw(game_surf)