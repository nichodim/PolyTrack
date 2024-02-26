from constants import *
from track_set_types import *
from track import Track

class TrackSet:
    def __init__(self, pos, type):
        self.structure = type
        self.tracks = []

        self.create_tracks(pos)
    

    # Track set game logic
    def create_tracks(self, pos):
        x, y = pos
        for instruction in self.structure:
            direction = instruction[0]
            image = instruction[1]

            # offset coordinates based on direction moved
            x += TrackOffset[direction][0]
            y += TrackOffset[direction][1]

            # Creates new track
            rect = pygame.Rect(x, y, TRACK_WIDTH, TRACK_HEIGHT)
            track = Track(image, rect)
            self.tracks.append(track)

            # Create relations between tracks
            if direction == 'origin': continue
            prev_track = self.tracks[len(self.tracks) - 1]
            track.set_relation(prev_track)
            prev_track.set_relation(track)

    def find_pos_of_tracks(self):
        positions = []
        for track in self.tracks:
            positions.append(track.rect.center)
        return positions

    def is_in_pos(self, pos):
        for track in self.tracks:
            if track.rect.collidepoint(pos): return True
        return False

    def attach_tracks_to_tiles(self, tiles):
        for i in range(len(tiles)):
            tile, track = tiles[i], self.tracks[i]
            tile.attach_track(track)
            track.rect.x = tile.rect.left
            track.rect.y = tile.rect.top

    # Moves tracks using direct position
    def set_position(self, pos):
        x, y = pos
        origin_track = self.tracks[0]
        delta_x = x - origin_track.rect.left
        delta_y = y - origin_track.rect.top
        self.move((delta_x, delta_y))
    # Moves tracks using relative position
    def move(self, relative_position):
        for track in self.tracks:
            track.move(relative_position)


    # Rendering
    def draw(self, game_surf):
        self.draw_tiles(game_surf)

    def draw_tiles(self, game_surf):
        for track in self.tracks:
            scaled_image = pygame.transform.scale(track.image, (TRACK_WIDTH, TRACK_HEIGHT))
            game_surf.blit(scaled_image, track.rect)
    
