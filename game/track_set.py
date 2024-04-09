import math
from constants import *
from track_set_types import *
from track import Track

class TrackSet:
    def __init__(self, pos, type):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.structure = type
        self.tracks = []

        self.create_tracks(pos)
    

    # Track set game logic
    def create_rect(self, origin_pos, positions):
        left, top = origin_pos[0], origin_pos[1]
        w, h = 0, 0

        used_x, used_y = [], []
        for pos in positions:
            x, y = pos[0][0], pos[0][1]
            direction = pos[1]

            if not x in used_x: 
                offset = TrackOffset[direction][0]
                if direction == 'origin': offset = width_and_gap

                if x < left: left = x
                w += math.fabs(offset)

                used_x.append(x)
            if not y in used_y: 
                offset = TrackOffset[direction][1]
                if direction == 'origin': offset = height_and_gap

                if y < top: top = y
                h += math.fabs(offset)

                used_y.append(y)

        self.rect = pygame.Rect(left, top, w, h)
        
    def create_tracks(self, pos):
        x, y = pos
        positions = []
        for instruction in self.structure:
            direction = instruction[0]
            data = instruction[1]

            # offset coordinates based on direction moved
            x += TrackOffset[direction][0]
            y += TrackOffset[direction][1]

            # Creates new track
            rect = pygame.Rect(x, y, TRACK_WIDTH, TRACK_HEIGHT)
            track = Track(rect, data)
            self.tracks.append(track)
            positions.append(((rect.left, rect.top), direction))

            # Create relations between tracks
            if direction == 'origin': continue
            prev_track = self.tracks[len(self.tracks) - 1]
            track.set_relation(prev_track)
            prev_track.set_relation(track)
        
        self.create_rect(pos, positions)

    def find_pos_of_tracks(self):
        positions = []
        for track in self.tracks:
            positions.append(track.rect.center)
        return positions
    def find_precise_pos_of_tracks(self):
        positions = []
        for track in self.tracks:
            pos = (track.rect.topleft, track.rect.bottomright)
            positions.append(pos)
        return positions
    
    def find_track_in_pos(self, pos):
        for track in self.tracks:
            is_in_pos = track.rect.collidepoint(pos)
            if is_in_pos: return track
        return None
    
    def is_in_pos(self, pos):
        for track in self.tracks:
            if track.rect.collidepoint(pos): return True
        return False
    
    def track_set_over_rect(self, rect):
        positions = [ self.rect.topright, self.rect.topleft, self.rect.bottomright, self.rect.bottomleft ]

        for pos in positions:
            side_in_rect = rect.collidepoint(pos)
            if not side_in_rect: return False
        return True
    def tracks_over_rect(self, rect):
        positions = self.find_pos_of_tracks()
        
        for pos in positions:
            track_in_rect = rect.collidepoint(pos)
            if not track_in_rect: return False
        return True
    
    def track_set_at_all_over_rect(self, rect):
        positions = [ self.rect.topright, self.rect.topleft, self.rect.bottomright, self.rect.bottomleft ]

        for pos in positions:
            side_in_rect = rect.collidepoint(pos)
            if side_in_rect: return True
        return False

    def attach_tracks_to_tiles(self, tiles):
        for i in range(len(tiles)):
            tile, track = tiles[i], self.tracks[i]
            tile.attach(track)
            track.rect.x = tile.rect.left
            track.rect.y = tile.rect.top

    def set_position_by_track(self, pos, i):
        x, y = pos
        primary_track = self.tracks[i]
        delta_x = x - primary_track.rect.left
        delta_y = y - primary_track.rect.top
        self.move((delta_x, delta_y))
    def set_position_by_center(self, pos):
        delta_x = pos[0] - self.rect.centerx
        delta_y = pos[1] - self.rect.centery
        self.move((delta_x, delta_y))

    # Moves tracks using relative position
    def move(self, relative_position):
        self.rect.move_ip(relative_position)
        for track in self.tracks:
            track.move(relative_position)


    # Rendering
    def draw(self, game_surf):
        self.draw_tiles(game_surf)

    def draw_tiles(self, game_surf):
        for track in self.tracks:
            scaled_image = pygame.transform.scale(track.image, (TRACK_WIDTH, TRACK_HEIGHT))
            game_surf.blit(scaled_image, track.rect)