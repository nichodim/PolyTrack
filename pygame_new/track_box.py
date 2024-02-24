# The box holding and controlling the tracks - once tracks are placed on the board, tracks are no longer considered tracks

import random
from constants import *
from track import Track
from tile import Tile

class Trackbox:
    def __init__(self):
        # Create track box
        track_box_width = 5 * TRACK_WIDTH + (TRACK_SEPERATION - TRACK_WIDTH) * (5 - 1) + EXTRA_WIDTH * 4
        track_box_height = TRACK_HEIGHT + EXTRA_HEIGHT * 2
        track_box_x = GAME_WIDTH / 2 - track_box_width / 2
        track_box_y = GAME_HEIGHT * 0.85
        self.rect = pygame.Rect(track_box_x, track_box_y, track_box_width, track_box_height)

        # Create tracks
        self.tracks = []


    # Track box game logic
    def generate_new_tracks(self):  
        not_enough_tracks = len(self.tracks) < 5
        if not_enough_tracks:
            track_possibilities = [TrackSprites.horizontal_track, TrackSprites.vertical_track, TrackSprites.right_track, TrackSprites.left_track]
            track_x = self.rect.left + EXTRA_WIDTH * 2 + TRACK_SEPERATION * len(self.tracks)
            track_y = self.rect.centery - EXTRA_HEIGHT

            new_track = Track(
                image = random.choice(track_possibilities),
                rect = pygame.Rect(track_x, track_y, TRACK_WIDTH, TRACK_HEIGHT)
            )
            self.tracks.append(new_track)

    def try_attach_track_to_tile(self, tile, i):
        track = self.tracks[i]

        if tile.try_attach_track(track) == False:
            return False
        
        track.rect.x = tile.rect.left
        track.rect.y = tile.rect.top
        return True

    def move_track(self, i, relative_position):
        self.tracks[i].move_track(relative_position)
    
    def remove_track(self, i):
        self.tracks.pop(i)
        for j in range(i, len(self.tracks)):
            self.tracks[j].rect.x -= TRACK_SEPERATION

    def set_track_to_initial(self, i):
        self.tracks[i].rect.x = self.rect.left + EXTRA_WIDTH * 2 + TRACK_SEPERATION * i
        self.tracks[i].rect.y = self.rect.centery - EXTRA_HEIGHT

    def update(self):
        self.generate_new_tracks()


    # Rendering
    def draw(self, game_surf):
        self.draw_track_box(game_surf)
        self.draw_tracks(game_surf)

    def draw_track_box(self, game_surf):
        pygame.draw.rect(game_surf, Colors.black, self.rect)
    def draw_tracks(self, game_surf):
        for track in self.tracks:
            scaled_image = pygame.transform.scale(track.image, (TRACK_WIDTH, TRACK_HEIGHT))
            game_surf.blit(scaled_image, track.rect)