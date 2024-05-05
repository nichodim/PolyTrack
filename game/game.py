# The top level of a scene, this is the state where you actually play
import pygame
import sys
import random
import math
from constants import *
from board import Board
from track_box import Trackbox
from powerup_menu import PowerupMenu
from weather import Weather

class Game:
    def __init__(self, map):
        pygame.init()
        self.game_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.fps = pygame.time.Clock()

        self.paused = False

        self.board = Board(map, self.handle_board_end, self.handle_complete_map)

        self.track_box = Trackbox()

        self.active_set = None
        self.active_track_and_index = None

        self.powerup_menu = PowerupMenu(self.track_box.rect)
        self.active_powerup = None

        self.lives = 3
        self.winner = False
        self.loser = False

        self.saved_time = 0
        self.map = map

        print('lives:', self.lives)

        # Constant Particle Weather
        # This implementation only accounts for constant weather on map types
        self.weather = None
        if map['type'] == "frozen": self.weather = Weather("snow", direction="left", degree=45)



    # Event control 
    def handle_events(self):
        for event in pygame.event.get():
            # Events allowed when paused
            if self.paused: 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.handle_escape()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: self.handle_mouse_up()
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.handle_escape()
                if event.unicode == 'r': self.handle_r_down()
                if event.unicode == 'f': self.board.toggle_fast_forward(True)  
            elif event.type == pygame.KEYUP:
                if event.unicode == 'f': self.board.toggle_fast_forward(False)
            elif event.type == pygame.QUIT:
                self.quit_game()

    def activate_powerup(self, event):
        self.active_powerup = self.powerup_menu.find_powerup(event.pos)
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
        if activated: 
            self.board.highlight_color = Colors.red # TODO make this dependant on powerup type
            return

        # Otherwise, activates track set if possible
        activated = self.activate_set(event)
        if not activated: 
            self.active_set == None
            self.active_track_and_index == None
        self.track_box.handle_spawn_button()
        self.board.highlight_color = Colors.green

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

            if board_triggered: 
                self.powerup_menu.remove_powerup(self.active_powerup)
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
            self.try_highlight_tiles_by_set()
        elif self.active_powerup != None:
            self.active_powerup.move(event.rel)
            self.highlight_tiles_by_powerup()

    def handle_r_down(self):
        if self.active_set and self.active_track_and_index: 
            SFX.tick.play()

            self.active_set = self.track_box.rotate(
                track_set = self.active_set, 
                hovered_track_and_index = self.active_track_and_index, 
            )
            
            track_index = self.active_track_and_index[1]
            self.active_track_and_index = (self.active_set.tracks[track_index], track_index)

            self.try_highlight_tiles_by_set()

    def handle_escape(self):
        if self.active_set: return
        # Modified: Matthew Selvaggi
        # Date: 5-3-24
        # Edited to calculate the time in seconds before pause
        if not self.paused:
            current_time = pygame.time.get_ticks() / 1000
            self.saved_time = current_time

        self.paused = not self.paused
    def restart_game(self):
        self.saved_time = 0
        self.winner = False
        self.loser = False
        self.lives = 3
        self.paused = False

        pygame.quit()  # Clean up existing Pygame resources
        pygame.init()  # Reinitialize Pygame

        # Reinitialize game components
        self.game_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.fps = pygame.time.Clock()

        self.board = Board(self.map, self.handle_board_end, self.handle_complete_map)
        self.track_box = Trackbox()
        self.powerup_menu = PowerupMenu(self.track_box.rect)

        if self.map['type'] == "frozen":
            self.weather = Weather("snow", direction="left", degree=45)
        else:
            self.weather = None

    def handle_board_end(self, win):
        if not win: self.lives -= 1
        if win: 
            self.lives += 1

        print('lives:', self.lives)

        if self.lives <= 0:
            self.loser = True
            self.handle_escape()

    def handle_complete_map(self):
        print('You finished the map!')
        self.winner = True
        self.handle_escape()
    

    # Game logic between components
    def try_highlight_tiles_by_set(self):
        tiles = self.find_open_tiles_under_tracks()
        if not tiles: 
            self.board.unhighlight()
            return
        self.board.highlight(tiles)
    
    def highlight_tiles_by_powerup(self):
        tile = self.board.find_tile_in_location(self.active_powerup.rect.center)
        if not tile: 
            self.board.unhighlight()
            return

        if self.active_powerup.type_name == 'bomb' or self.active_powerup.type_name == 'bigbomb':
            self.board.highlight_bomb_tiles(self.active_powerup, tile)

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
        self.board.trigger_powerup(self.active_powerup, tile, self.game_surf)
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
        if self.weather != None: self.weather.update()

    # Author: Matthew Selvaggi
    # Date: 5-3-24
    # Purpose: Call for pause/win/lose menu with respective button images.
    def menu(self, button1_image, button1_image_hover, button2_image, button2_image_hover):
        # Initial box dimensions
        box_width = 700
        box_height = 400
        border_width = 5
        button_width = 250
        button_height = 100
        button_spacing = 50
        threshold = 50

        # Center of the box x,y
        box_x = (GAME_WIDTH - box_width) // 2
        box_y = (GAME_HEIGHT - box_height) // 2

        # Boarder to the box
        bordered_box_surf = pygame.Surface((box_width, box_height))
        bordered_box_surf.fill(Colors.black)
        blue_box_surf = pygame.Surface((box_width - 2 * border_width, box_height - 2 * border_width))
        blue_box_surf.fill(Colors.sky_blue)

        # Blit boxes
        self.game_surf.blit(bordered_box_surf, (box_x, box_y))
        self.game_surf.blit(blue_box_surf, (box_x + border_width, box_y + border_width))

        # Button position
        total_space = box_width - (2 * border_width)
        total_button_width = 2 * button_width + button_spacing
        available_space = total_space - total_button_width

        # Calculate x-cords for the buttons
        button_x1 = box_x + border_width + (available_space // 2)
        button_x2 = button_x1 + button_width + button_spacing

        button_y = box_y + (box_height - button_height) // 2

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Scale button images
        button_image_normal1 = pygame.transform.scale(button1_image, (button_width, button_height))
        button_image_hover1 = pygame.transform.scale(button1_image_hover, (button_width, button_height))
        button_image_normal2 = pygame.transform.scale(button2_image, (button_width, button_height))
        button_image_hover2 = pygame.transform.scale(button2_image_hover, (button_width, button_height))

        # Calculate distances to button centers
        distance_to_button1 = math.sqrt(
            (button_x1 + button_width / 2 - mouse_x) ** 2 + (button_y + button_height / 2 - mouse_y) ** 2)
        distance_to_button2 = math.sqrt(
            (button_x2 + button_width / 2 - mouse_x) ** 2 + (button_y + button_height / 2 - mouse_y) ** 2)

        # Change button to hover animation
        if distance_to_button1 < threshold:
            self.game_surf.blit(button_image_hover1, (button_x1, button_y))
        else:
            self.game_surf.blit(button_image_normal1, (button_x1, button_y))

        if distance_to_button2 < threshold:
            self.game_surf.blit(button_image_hover2, (button_x2, button_y))
        else:
            self.game_surf.blit(button_image_normal2, (button_x2, button_y))

        # Render Text
        font_time = pygame.font.Font('font/font.ttf', 36)
        font_message = pygame.font.Font('font/font.ttf', 45)
        elapsed_time_text = f'Time: {self.saved_time:.2f} seconds'
        text_surface = font_time.render(elapsed_time_text, True, (0, 0, 0))

        # Displays winner/loser if the game is completed
        if self.loser:
            result_message = f"Loser!"
            result_text = font_message.render(result_message, True, (255,0,0))
        elif self.winner:
            result_message = f"Winner!"
            result_text = font_message.render(result_message, True, (0,255,0))
        else:
            result_message = f"Paused"
            result_text = font_message.render(result_message, True, (0,0,0))
                
        # Text Position of Reult
        text_width = result_text.get_width()
        text_x = box_x + (box_width - text_width) // 2
        text_y = box_y + 50

        self.game_surf.blit(result_text, (text_x, text_y))


        # Text Position of Time
        text_width = text_surface.get_width()
        text_x = box_x + (box_width - text_width) // 2
        text_y = box_y + 280

        self.game_surf.blit(text_surface, (text_x, text_y))

        # Check for button clicks
        if distance_to_button1 < threshold and pygame.mouse.get_pressed()[0]:
            self.restart_game()
        elif distance_to_button2 < threshold and pygame.mouse.get_pressed()[0]:
            self.quit_game()

    def render(self):
        self.game_surf.fill(Colors.sky_blue)
        self.board.draw(self.game_surf)
        self.powerup_menu.draw(self.game_surf)
        self.track_box.draw(self.game_surf)
        if self.weather != None: self.weather.draw(self.game_surf)

        # Paused render
        if self.paused:
            highlight_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            r, g, b = Colors.light_gray
            highlight_surf.fill((r, g, b, 128))
            self.game_surf.blit(highlight_surf, (0, 0))
            # Modified: Matthew Selvaggi
            # Date: 5-3-24
            # Purpose: Addded condition to check if the user is winning, losing, or paused.
            # This will allow the program to generate the approriate button images depending on the action.
            if self.winner:
                pass
            elif self.loser:
                self.menu(Images.restart_img, Images.restart_hover, Images.quit_pause_img, Images.quit_pause_hover_img )
                # Render Text
                font = pygame.font.Font('font/font.ttf', 36)
                elapsed_time_text = f'Time: {self.saved_time:.2f} seconds'

            else:
                self.menu(Images.play_img, Images.play_hover_img, Images.quit_pause_img, Images.quit_pause_hover_img )


        pygame.display.update()