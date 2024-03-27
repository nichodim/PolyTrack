# The top level of a scene, this is the state where you actually play

import pygame
import sys
import random
from constants import *
from board import Board
from track_box import Trackbox

class Game:
    def __init__(self):
        pygame.init()
        self.game_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.fps = pygame.time.Clock()

        self.board = Board(self.handle_board_end)

        self.track_box = Trackbox()
        self.active_set = None
        self.active_track_and_index = None

        self.lives = 50
        print('lives:', self.lives)


    # Event control 
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: self.handle_mouse_up()
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            elif event.type == pygame.KEYDOWN:
                if event.unicode == 'r': self.handle_r_down()
            elif event.type == pygame.QUIT:
                self.quit_game()

    def activate_set(self, event):
        # Find picked up track set and the hovered track/index
        self.active_set = self.track_box.find_track_set(event.pos)
        if not self.active_set: return False

        # Something crazy is going on with the pickup so cancel before crash
        # Likely because mouse pos cannot find track and index (wild movement)
        self.active_track_and_index = self.track_box.find_hovered_track_and_index(self.active_set)
        if self.active_track_and_index == None: return False

        SFX.metal_move.play()

        self.active_set_inital_pos = self.active_set.rect.center

        # Aligns the hovered track with the mouse for easy rotation
        # Very difficult to naturally rotate without this
        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_pos = (mouse_x - TRACK_WIDTH // 2, mouse_y - TRACK_HEIGHT // 2)
        self.active_set.set_position_by_track(new_pos, self.active_track_and_index[1])
        return True
    
    def handle_mouse_down(self, event):
        # Activates new set and track/index, if failed, abort
        activated = self.activate_set(event)
        if not activated: 
            self.active_set == None
            self.active_track_and_index == None
        
        self.track_box.handle_spawn_button()

    def handle_mouse_up(self):
        def clear_active_set():
            self.board.unhighlight()
            self.active_set = None
            self.active_track_and_index = None
            self.active_set_inital_pos = None

        if self.active_set == None: return

        # Snaps board and finds if track set should be set back to initial position
        set_snapped = self.snap_set_to_board()
        over_track_spawner = self.active_set.track_set_over_rect(self.track_box.spawner.rect)
        over_track_box = self.active_set.track_set_over_rect(self.track_box.rect)

        if set_snapped: 
            self.track_box.update_spawner(self.active_set)
            random.choice([SFX.smalldrill, SFX.smalldrill, SFX.doubledrill]).play()
            clear_active_set()
            return

        if over_track_box and not over_track_spawner: 
            self.track_box.update_spawner(self.active_set)
            random.choice([SFX.small_metal_drop, SFX.small_metal_drop, SFX.med_metal_drop]).play()
            clear_active_set()
            return
        
        self.active_set.set_position_by_center(self.active_set_inital_pos)
        clear_active_set()

    def handle_mouse_motion(self, event):
        if self.active_set != None:
            self.active_set.move(event.rel)
            self.try_highlight_tiles()
    
    def handle_r_down(self):
        if self.active_set and self.active_track_and_index: 
            SFX.tick.play()

            self.active_set = self.track_box.rotate(
                track_set = self.active_set, 
                hovered_track_and_index = self.active_track_and_index, 
            )
            
            track_index = self.active_track_and_index[1]
            self.active_track_and_index = (self.active_set.tracks[track_index], track_index)

            self.try_highlight_tiles()

    def handle_board_end(self, win):
        if not win: self.lives -= 1
        if win: 
            self.lives += 1
            print('noice ;)')

        print('lives:', self.lives)

        if self.lives <= 0:
            print('you lost')
            self.quit_game()
    

    # Game logic between components
    def try_highlight_tiles(self):
        tiles = self.find_open_tiles_under_tracks()
        if not tiles: 
            self.board.unhighlight()
            return
        self.board.highlight(tiles)

    def find_open_tiles_under_tracks(self):
        track_positions = self.active_set.find_pos_of_tracks()
        tiles = []
        for position in track_positions:
            tile = self.board.find_tile_in_location(position)

            if tile == None: return None
            if not tile.is_open(): return None
            tiles.append(tile)
        return tiles

    def snap_set_to_board(self):
        hovered_tiles = self.find_open_tiles_under_tracks()
        if not hovered_tiles: return False
        self.active_set.attach_tracks_to_tiles(hovered_tiles)
        self.track_box.track_sets.remove(self.active_set)
        return True


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
        self.board.update()
        
        
    def render(self):
        self.game_surf.fill(Colors.dark_gray)
        
        self.board.draw(self.game_surf)
        self.track_box.draw(self.game_surf)
        
        self.board.update()

        pygame.display.update()