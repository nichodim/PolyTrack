from constants import *
from track_set_types import *
from track import Track

class TrackSet:
    def __init__(self, pos, type):
        self.origin_x, self.origin_y = pos
        self.structure = TrackSetTypes[type]
        self.tracks = []

        self.create_tracks()
    
    def create_tracks(self):
        x, y = self.origin_x, self.origin_y
        for instruction in self.structure:
            direction = instruction[0]
            image = instruction[1]

            # Creates new track
            rect = pygame.Rect(x, y, TRACK_WIDTH, TRACK_HEIGHT)
            track = Track(image, rect)
            self.tracks.append(track)

            # Create relations between tracks
            if direction == 'origin': continue
            prev_track = self.tracks[len(self.tracks) - 1]
            track.set_relation(prev_track)
            prev_track.set_relation(track)

            # offset coordinates based on direction moved
            x += TrackOffset[direction][0]
            y += TrackOffset[direction][1]
    
