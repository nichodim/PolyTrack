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
from button import Button
import maps

# Modified: Matthew Selvaggi
# Date: 5-29-24
# Purpose: In order to avoid a circular loop, needed to place menu
# inside of game.
class Menu:
    def map_menu(self):
        pygame.init()

        button_x = GAME_WIDTH / 4
        map_button_radius = Images.mapmenu_img.get_width()
        image_scale = 3
        button_radius = Images.grass_map.get_width()

        center_x = GAME_WIDTH / 2
        button_width = button_radius * image_scale

        gap = (GAME_WIDTH - 2 * button_width) / 6
        grass_map_x = center_x - button_width - gap / 2
        snow_map_x = center_x + gap / 3

        grass_map = Button(grass_map_x, 400, Images.grass_map, image_scale)
        snow_map = Button(snow_map_x, 400, Images.snow_map, image_scale)
        map_img = Button(2 * button_x - map_button_radius, 100, Images.mapmenu_img, 2)

        render = True
        run = True

        while run:
            main_surf.fill(Colors.sky_blue)
            grass_map.draw(main_surf)
            snow_map.draw(main_surf)
            map_img.draw(main_surf)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if grass_map.clicked():
                        self.GrassMapSizeMenu()
                        render = False
                    if snow_map.clicked():
                        self.SnowMapSizeMenu()
                        render = False

            if render:
                pygame.display.update()


    def GrassMapSizeMenu(self):
        pygame.init()

        image_scale = 3
        button_x = GAME_WIDTH / 4
        button_radius = Images.grass_map_small.get_width() * 3 / 2
        map_button_radius = Images.select_size_img.get_width() / 2
        Grass_small = Button(button_x - button_radius, 400, Images.grass_map_small, image_scale)
        Grass_medium = Button(2 * button_x - button_radius, 400, Images.grass_map_medium, image_scale)
        Grass_large = Button(3 * button_x - button_radius, 400, Images.grass_map_large, image_scale)
        select_size = Button(2 * button_x - map_button_radius, 100, Images.select_size_img, 1)

        run = True
        while run:
            main_surf.fill(Colors.sky_blue)
            Grass_small.draw(main_surf)
            Grass_medium.draw(main_surf)
            Grass_large.draw(main_surf)
            select_size.draw(main_surf)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Grass_small.clicked():
                        game = Game(maps.GrassMapSmall)
                        game.run()
                    if Grass_medium.clicked():
                        game = Game(maps.GrassMapMedium)
                        game.run()
                    if Grass_large.clicked():
                        game = Game(maps.GrassMapLarge)
                        game.run()

            pygame.display.update()


    def SnowMapSizeMenu(self):
        pygame.init()

        image_scale = 3
        button_x = GAME_WIDTH / 4
        button_radius = Images.snow_map_small.get_width() * 3 / 2
        map_button_radius = Images.select_size_img.get_width() / 2
        Snow_small = Button(button_x - button_radius, 400, Images.snow_map_small, image_scale)
        Snow_medium = Button(2 * button_x - button_radius, 400, Images.snow_map_medium, image_scale)
        Snow_large = Button(3 * button_x - button_radius, 400, Images.snow_map_large, image_scale)
        select_size = Button(2 * button_x - map_button_radius, 100, Images.select_size_img, 1)

        run = True
        while run:
            main_surf.fill(Colors.sky_blue)
            Snow_small.draw(main_surf)
            Snow_medium.draw(main_surf)
            Snow_large.draw(main_surf)
            select_size.draw(main_surf)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Snow_small.clicked():
                        game = Game(maps.SnowMapSmall)
                        game.run()
                    if Snow_medium.clicked():
                        game = Game(maps.SnowMapMedium)
                        game.run()
                    if Snow_large.clicked():
                        game = Game(maps.SnowMapLarge)
                        game.run()

            pygame.display.update()

class Game:
    def __init__(self, map):
        # Game initialization, i.e. board, trackbox, train
        pygame.init()
        self.map = map
        self.game_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.fps = pygame.time.Clock()
        self.board = Board(self.map, self.handle_board_end, self.handle_complete_map, self.animate_weather, self.game_surf)
        self.track_box = Trackbox()
        self.active_set = None
        self.active_track_and_index = None

        # Powerups
        self.powerup_menu = PowerupMenu(self.track_box.rect)
        self.active_powerup = None

        # Pause menu initialization
        self.lives = 5
        self.points = 0
        self.initial_lives = self.lives
        self.resume = True
        self.paused = False
        self.winner = False
        self.loser = False
        self.saved_time = 0

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
                if event.unicode.lower() == 'r': self.handle_r_down()
                if event.unicode.lower() == 'f': self.board.toggle_fast_forward(True)  
            elif event.type == pygame.KEYUP:
                if event.unicode.lower() == 'f': self.board.toggle_fast_forward(False)
            elif event.type == pygame.QUIT:
                self.quit_game()

    def activate_powerup(self, event):
        self.active_powerup = self.powerup_menu.find_powerup(event.pos)
        if not self.active_powerup: return False

        SFX.pickup2.play()
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
        self.board.active_tile_highlight = 'track'

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
            worked = self.try_highlight_tiles_by_powerup()
            if not worked: self.highlight_board_by_powerup()

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
        self.lives = self.initial_lives
        self.paused = False
        
        menu = Menu()
        menu.map_menu()
 
    def handle_board_end(self, win):
        if not win: self.lives -= 1
        if win: 
            self.lives += 1
            self.points += 1

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
    
    def try_highlight_tiles_by_powerup(self):
        tile = self.board.find_tile_in_location(self.active_powerup.rect.center)
        if not tile: 
            self.board.unhighlight()
            return False

        if self.active_powerup.type_name == 'bomb' or self.active_powerup.type_name == 'bigbomb':
            self.board.highlight_bomb_tiles(self.active_powerup, tile)
            return True
        
        if self.active_powerup.type_name == 'slow':
            self.board.highlight_slow_tiles(self.active_powerup, tile)
            return True
        
        # Sets individual path to hover freeze, saves if frozen to previous state
        if self.active_powerup.type_name == 'freeze':
            if len(self.board.paths) == 1: return False

            for path in self.board.paths:
                if 'hover' in path.highlight: 
                    path.highlight = path.prev_highlight

            path = tile.under_path
            if path != None:
                if path.highlight != '' and 'hover' not in path.highlight: 
                    path.prev_highlight = path.highlight
                path.highlight = 'freeze-hover'
                self.board.full_freeze = False
                return True

    def highlight_board_by_powerup(self):
        # Reverts path highlights if all hovered, leaves
        if not self.active_powerup.powerup_over_rect(self.board.rect):
            all_hovered = True
            for path in self.board.paths:
                if 'hover' not in path.highlight:
                    all_hovered = False
                    break
            
            if all_hovered:
                for path in self.board.paths:
                    path.highlight = path.prev_highlight
                    path.prev_highlight = ''
            return
        
        # Sets all paths to frozen highlight hover, saves frozen states to previous
        if self.active_powerup.type_name == 'freeze':
            for path in self.board.paths:
                if path.highlight != '' and 'hover' not in path.highlight: 
                    path.prev_highlight = path.highlight
                path.highlight = 'freeze-hover'
            self.board.full_freeze = True

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
        worked = self.board.trigger_powerup(self.active_powerup, tile, self.game_surf)
        return worked


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

    def animate_weather(self, w_type, duration = 3):
        self.weather.start_animation(w_type, duration)
    
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
            SFX.bleep.play()
            if self.resume:
                self.paused = not self.paused
            else:
                self.restart_game()

        elif distance_to_button2 < threshold and pygame.mouse.get_pressed()[0]:
            SFX.bleep.play()
            self.quit_game()
    
    # Author: Neo Chen
    # Date: 5-16-2024
    # Purpose: Displays internal points counter and lives counter
    def points_and_lives(self):
        points_font = pygame.font.Font('font/font.ttf', 30)
        points_text = points_font.render(f'Points: {self.points}', True, Colors.black, Colors.sky_blue)
        points_rect = points_text.get_rect()
        points_rect.topleft = (10, 4)

        lives_font = pygame.font.Font('font/font.ttf', 30)
        lives_text = lives_font.render(f'Lives: {self.lives}', True, Colors.black, Colors.sky_blue)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (10, 39)

        self.game_surf.blit(lives_text, lives_rect)
        self.game_surf.blit(points_text, points_rect)

    
    def render(self):
        self.game_surf.fill(Colors.sky_blue)
        self.board.draw(self.game_surf)
        self.powerup_menu.draw(self.game_surf)
        self.track_box.draw(self.game_surf)
        self.points_and_lives()
        if self.weather != None: self.weather.draw(self.game_surf)

        # Paused render
        if self.paused:
            highlight_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            r, g, b = Colors.light_gray
            highlight_surf.fill((r, g, b, 128))
            self.game_surf.blit(highlight_surf, (0, 0))

            # Modified: Matthew Selvaggi
            # Date: 5-3-24
            # Purpose: Added condition to check if the user is winning, losing, or paused.
            # This will allow the program to generate the appropriate button images depending on the action.
            if self.winner or self.loser:                                                                                  # Modified: Matthew Selvaggi
                self.resume = False                                                                                        # Date: 5-6-24
                self.menu(Images.restart_img, Images.restart_hover, Images.quit_pause_img, Images.quit_pause_hover_img)    # Added logic for winner actions menu
                # Render Text
                font = pygame.font.Font('font/font.ttf', 36)
                elapsed_time_text = f'Time: {self.saved_time:.2f} seconds'
            else:
                self.resume = True
                self.menu(Images.play_img, Images.play_hover_img, Images.quit_pause_img, Images.quit_pause_hover_img )


        pygame.display.update()