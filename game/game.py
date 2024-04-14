# The top level of a scene, this is the state where you actually play

import pygame
import sys
import random
from constants import *
from board import Board
from track_box import Trackbox
from powerup import Powerup
import math

class Game:
    def __init__(self, map):
        pygame.init()
        self.game_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.fps = pygame.time.Clock()

        self.f_pressed = False
        self.paused = False

        self.board = Board(map, self.handle_board_end, self.handle_complete_map)
        self.track_box = Trackbox()

        self.active_set = None
        self.active_track_and_index = None

        self.active_powerup = None
        self.track_box.generate_powerup()

        self.lives = 50
        print('lives:', self.lives)


    # Event control 
    def handle_events(self):
        for event in pygame.event.get():
            # Events allowed when paused
            if self.paused: 
                if event.type == pygame.KEYDOWN:
                    if event.unicode == 'p': self.handle_p_down()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: self.handle_mouse_up()
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            elif event.type == pygame.KEYDOWN:
                if event.unicode == 'r': self.handle_r_down()
                if event.unicode == 'p': self.handle_p_down()
                if event.unicode == 'f':
                    self.board.set_f_pressed(True)
                    self.board.update_path_f_pressed(True)
                    
            elif event.type == pygame.KEYUP:
                if event.unicode == 'f':
                    self.board.set_f_pressed(False)
                    self.board.update_path_f_pressed(False)
            elif event.type == pygame.QUIT:
                self.quit_game()

    def activate_powerup(self, event):
        self.active_powerup = self.track_box.find_powerup(event.pos)
        if not self.active_powerup: return False

        SFX.metal_move.play() # TODO replace with proper sound
        self.active_powerup_inital_pos = self.active_powerup.rect.center

        return True

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
        # Activates powerup if possible
        activated = self.activate_powerup(event)
        if activated: return

        # Otherwise, activates track set if possible
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
        def clear_active_powerup():
            self.active_powerup_inital_pos = None
            self.active_powerup = None

        if self.active_set == None: 
            if self.active_powerup == None: return

            board_triggered = self.trigger_powerup_on_board()
            over_track_spawner = self.active_powerup.powerup_over_rect(self.track_box.spawner.rect)
            over_track_box = self.active_powerup.powerup_over_rect(self.track_box.rect)

            if board_triggered: 
                self.track_box.powerups.remove(self.active_powerup)
                clear_active_powerup()
                return

            if over_track_box and not over_track_spawner:
                clear_active_powerup()
                return

            self.active_powerup.set_position_by_center(self.active_powerup_inital_pos)
            clear_active_powerup()
            return

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
        elif self.active_powerup != None:
            self.active_powerup.move(event.rel)
            # self.try_highlight_tiles()

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

    def handle_p_down(self):
        if self.active_set: return
        self.paused = not self.paused

    def handle_board_end(self, win):
        if not win: self.lives -= 1
        if win: 
            self.lives += 1
            print('noice ;)')

        print('lives:', self.lives)

        if self.lives <= 0:
            print('you lost')
            self.quit_game()
    
    def handle_complete_map(self):
        print('You finished the map!')
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
    
    def trigger_powerup_on_board(self):
        tile = self.board.find_tile_in_location(self.active_powerup.rect.center)
        if not tile: return False
        self.board.trigger_powerup(self.active_powerup, tile)
        return True


    # Boilerplate to functionally update the game
    def quit_game(self):
        pygame.quit()
        sys.exit()
    
    def run(self):
        while True:
            self.handle_events()
            if not self.paused: self.update()
            self.render()
            self.fps.tick(60)

    def update(self):
        self.board.update()
        
        
    def render(self):
        self.game_surf.fill(Colors.dark_gray)
        self.board.draw(self.game_surf)
        self.track_box.draw(self.game_surf)

        # Paused render
        if self.paused:
            highlight_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            r, g, b = Colors.light_gray
            highlight_surf.fill((r, g, b, 128))
            self.game_surf.blit(highlight_surf, (0, 0))

            box_width = 700
            box_height = 400
            border_width = 5

            bordered_box_surf = pygame.Surface((box_width, box_height))
            bordered_box_surf.fill(Colors.black)

            blue_box_surf = pygame.Surface((box_width - 2 * border_width, box_height - 2 * border_width))
            blue_box_surf.fill(Colors.sky_blue)

            # Calculate the position for the bordered box
            box_x = (GAME_WIDTH - box_width) // 2 - 2
            box_y = (GAME_HEIGHT - box_height) // 2 - 90

            self.game_surf.blit(bordered_box_surf, (box_x, box_y))

            self.game_surf.blit(blue_box_surf, (box_x + border_width, box_y + border_width))

            # Button dimensions and positions
            button_width = 250
            button_height = 100
            button_y = box_y + (box_height - button_height) // 2

            button_x1 = box_x + (box_width - button_width * 2) // 3
            button_x2 = button_x1 + button_width + (box_width - button_width * 2) // 3

            mouse_x, mouse_y = pygame.mouse.get_pos()
 
            button1_image = Images.play_img
            button1_image_hover = Images.play_hover_img

            button2_image = Images.quit_pause_img
            button2_image_hover = Images.quit_pause_hover_img

            button_image_normal1 = pygame.transform.scale(button1_image, (button_width, button_height))
            button_image_hover1 = pygame.transform.scale(button1_image_hover, (button_width, button_height))

            button_image_normal2 = pygame.transform.scale(button2_image, (button_width, button_height))
            button_image_hover2 = pygame.transform.scale(button2_image_hover, (button_width, button_height))

            threshold = 50

            # Calculate the distance between the mouse and button centers
            distance_to_button1 = math.sqrt((button_x1 + button_width / 2 - mouse_x) ** 2 + (button_y + button_height / 2 - mouse_y) ** 2)
            distance_to_button2 = math.sqrt((button_x2 + button_width / 2 - mouse_x) ** 2 + (button_y + button_height / 2 - mouse_y) ** 2)

            if distance_to_button1 < threshold:
                self.game_surf.blit(button_image_hover2, (button_x1, button_y))
            else:
                self.game_surf.blit(button_image_normal2, (button_x1, button_y))

            if distance_to_button2 < threshold:
                self.game_surf.blit(button_image_hover1, (button_x2, button_y))
            else:
                self.game_surf.blit(button_image_normal1, (button_x2, button_y))


            # Check for button clicks
            if distance_to_button1 < threshold and pygame.mouse.get_pressed()[0]:
                self.quit_game()

            elif distance_to_button2 < threshold and pygame.mouse.get_pressed()[0]:
                self.paused = False

        pygame.display.update()

        pygame.display.update()