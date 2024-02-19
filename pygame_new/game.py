# The top level of a scene, this is the state where you actually play

import pygame
import sys
import random
from constants import *
from board import Board
from track_box import Trackbox
from tile import Tile

class Game:
    def __init__(self):
        pygame.init()
        self.game_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.fps = pygame.time.Clock()

        self.board = Board()

        self.track_box = Trackbox()
        self.active_track = None


    # Event control 
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
        for num, track in enumerate(self.track_box.tracks):
            if track.rect.collidepoint(event.pos):
                self.active_track = num

    def handle_mouse_up(self, event):
        if self.active_track != None:
            self.try_snap_track_to_board(event)
            self.active_track = None

    def handle_mouse_motion(self, event):
        if self.active_track != None:
            self.track_box.move_track(self.active_track, event.rel)
    

    # Game logic between components
    def try_snap_track_to_board(self, event):
        hovered_tile = self.board.find_tile_in_location(event.pos)
        if hovered_tile == None:
            self.track_box.set_track_to_initial(self.active_track)
            return
        
        did_track_attach = self.track_box.try_attach_track_to_tile(hovered_tile, self.active_track)
        if did_track_attach == False:
            self.track_box.set_track_to_initial(self.active_track)
            return
        
        self.track_box.remove_track(self.active_track)


    # Boilerplate to functionally update the game
    def quit_game(self):
        pygame.quit()
        sys.exit()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.fps.tick(60)

    def update(self):
        self.track_box.update()

    def render(self):
        self.game_surf.fill(Colors.dark_gray)
        
        self.board.draw(self.game_surf)
        self.track_box.draw(self.game_surf)

        pygame.display.update()