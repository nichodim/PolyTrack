# The top level of the game, this is the state where you actually play

import pygame
import sys
import random
from constants import *
from board import Board
from track import Track

class Game:
    def __init__(self):
        pygame.init()
        self.game_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.fps = pygame.time.Clock()
        self.board = Board()
        self.tracks = []
        self.active_track = None
        self.tracks_in_box = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: self.handle_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            elif event.type == pygame.QUIT:
                self.quit_game()

    def handle_mouse_down(self, event):
        for num, track in enumerate(self.tracks):
            if track.rect.collidepoint(event.pos):
                self.detach_track_from_grid(track)
                self.active_track = num

    def handle_mouse_up(self, event):
        if self.active_track != None:
            self.try_snap_track_to_grid(event)
            self.active_track = None

    def handle_mouse_motion(self, event):
        if self.active_track != None:
            self.tracks[self.active_track].move_track(event.rel)

    def detach_track_from_grid(self, track):
        for i, row in enumerate(self.board.tiles):
            for j, tile in enumerate(row):
                if tile.attached_track == track:
                    self.board.tiles[i][j].attached_track = None

    def try_snap_track_to_grid(self, event):
        # Check if pointer over an empty board tile
        #   -> Snap track to board tile and link track to tile

        # Calculate the nearest row and column
        precice_row = ((event.pos[1] - self.board.rect.top - OUTER_GAP) - NUM_ROWS * ((event.pos[1] - self.board.rect.top - OUTER_GAP) // 55)) // 50
        precice_column = ((event.pos[0] - self.board.rect.left - OUTER_GAP) - NUM_COLS * ((event.pos[0] - self.board.rect.left - OUTER_GAP) // 55)) // 50

        if (
            0 <= precice_row <= NUM_ROWS - 1 and # valid row
            0 <= precice_column <= NUM_COLS - 1 and # valid column
            self.board.tiles[precice_row][precice_column].rect.collidepoint(event.pos) and # over tile
            not self.board.tiles[precice_row][precice_column].attached_track # tile empty
        ): 
            # Set track to tile underneath
            self.tracks[self.active_track].rect.x = self.board.tiles[precice_row][precice_column].rect.left
            self.tracks[self.active_track].rect.y = self.board.tiles[precice_row][precice_column].rect.top
            self.board.tiles[precice_row][precice_column].attached_track = self.tracks[self.active_track]

            # 
            self.tracks.pop(self.active_track)
            for i in range(self.active_track, len(self.tracks)):
                self.tracks[i].rect.x -= TRACK_SEPERATION
            
        # send the track back to it initial position if it fails to snap to the grid
        else:
            self.tracks[self.active_track].rect.x = self.board.track_box.left + EXTRA_WIDTH * 2 + TRACK_SEPERATION * self.active_track
            self.tracks[self.active_track].rect.y = self.board.track_box.centery - EXTRA_HEIGHT

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run_game(self):
        while True:
            self.handle_events()
            self.update_game()
            self.render_game()
            self.fps.tick(60)

    def update_game(self):
        #self.board.update_tracks_in_grid(self.tracks)
        self.generate_new_tracks()

    def render_game(self):
        self.game_surf.fill(Colors.dark_gray)
        self.board.draw_board(self.game_surf)
        self.board.draw_tracks_on_board(self.game_surf)
        self.board.draw_track_box(self.game_surf, self.tracks)
        pygame.display.update()

    def generate_new_tracks(self):  
        # and pygame.time.get_ticks() % 50 == 0

        if len(self.tracks) < 5:
            track_possibilities = [TrackTypes.horizontal_track, TrackTypes.straight_track, TrackTypes.right_track, TrackTypes.left_track]
            track_x = self.board.track_box.left + EXTRA_WIDTH * 2 + TRACK_SEPERATION * len(self.tracks)
            track_y = self.board.track_box.centery - EXTRA_HEIGHT

            new_track = Track(
                image=random.choice(track_possibilities),
                rect=pygame.Rect(track_x, track_y, TRACK_WIDTH, TRACK_HEIGHT)
            )
            self.tracks.append(new_track)