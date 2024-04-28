# Constants used throughout the game

import pygame

# Constant variables - things you would configure
# Resolution config
GAME_WIDTH = 1400
GAME_HEIGHT = 900

# Board config
# Number of cols, rows has been depracated - determined by map
OUTER_BORDER_SIZE = 150
# NUM_ROWS = 10
# NUM_COLS = 10
INNER_GAP = 1
OUTER_GAP = 35

# Trackbox config
TRACK_WIDTH = 50
TRACK_HEIGHT = 50
TRACK_SEPERATION = TRACK_WIDTH * 2
EXTRA_WIDTH = TRACK_WIDTH * 0.75
EXTRA_HEIGHT = TRACK_HEIGHT / 2

main_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.init()

class SFX:
    pop = pygame.mixer.Sound('sfx/pop.mp3')
    ping = pygame.mixer.Sound('sfx/ping.mp3')
    metal_move = pygame.mixer.Sound('sfx/metal_move.mp3')
    small_metal_drop = pygame.mixer.Sound('sfx/small_metal_drop.mp3')
    med_metal_drop = pygame.mixer.Sound('sfx/med_metal_drop.mp3')
    smalldrill = pygame.mixer.Sound('sfx/smalldrill.mp3')
    doubledrill = pygame.mixer.Sound('sfx/doubledrill.mp3')
    drill = pygame.mixer.Sound('sfx/drill.mp3')
    pickup = pygame.mixer.Sound('sfx/pickup.mp3')
    tick = pygame.mixer.Sound('sfx/tick.mp3')
    theme_song = 'sfx/theme_song.mp3'
    explosion = pygame.mixer.Sound('sfx/explosion.mp3')

# Mixer
SFX.metal_move.set_volume(0.2)
SFX.small_metal_drop.set_volume(0.4)
SFX.med_metal_drop.set_volume(0.4)
SFX.smalldrill.set_volume(0.4)
SFX.doubledrill.set_volume(0.4)
SFX.tick.set_volume(0.15)

class Images:
    start_img = pygame.image.load('images/button_images/start.png').convert_alpha()
    start_hover_img = pygame.image.load('images/button_images/start_hover.png').convert_alpha()
    quit_img = pygame.image.load('images/button_images/quit.png').convert_alpha()
    quit_hover_img = pygame.image.load('images/button_images/quit_hover.png').convert_alpha()
    title_img = pygame.image.load('images/button_images/PolyTracks.png').convert_alpha()
    play_img = pygame.image.load('images/button_images/play_button.png').convert_alpha()
    play_hover_img = pygame.image.load('images/button_images/play_hover.png').convert_alpha()
    quit_pause_img = pygame.image.load('images/button_images/quit_button.png').convert_alpha()
    quit_pause_hover_img = pygame.image.load('images/button_images/quit_pause_hover.png').convert_alpha()
    snow_map = pygame.image.load('images/button_images/snow_mapbutton.png').convert_alpha()
    snow_map_large = pygame.image.load('images/button_images/snow_map_L.png').convert_alpha()
    snow_map_medium = pygame.image.load('images/button_images/snow_map_medium.png').convert_alpha()
    snow_map_small = pygame.image.load('images/button_images/snow_map_small.png').convert_alpha()
    grass_map = pygame.image.load('images/button_images/grass_mapbutton.png').convert_alpha()
    grass_map_small = pygame.image.load('images/button_images/grass_map_small.png').convert_alpha()
    grass_map_medium = pygame.image.load('images/button_images/grass_map_medium.png').convert_alpha()
    grass_map_large = pygame.image.load('images/button_images/grass_map_large.png').convert_alpha()
    mapmenu_img = pygame.image.load('images/button_images/MAPS.png').convert_alpha()
    select_size_img = pygame.image.load('images/button_images/select_map_size.png').convert_alpha()

class Toolbox:
    toolbox_sprite = pygame.image.load('images/toolbox_images/toolbox_sprite.png').convert_alpha()

class TrackSprites:
    horizontal = pygame.image.load('images/track_images/horizontal_track.png').convert_alpha()
    vertical = pygame.image.load('images/track_images/vertical_track.png').convert_alpha()
    right = pygame.image.load('images/track_images/right_track.png').convert_alpha()
    left = pygame.image.load('images/track_images/left_track.png').convert_alpha()
    inverted_right = pygame.image.load('images/track_images/inverted_right_track.png').convert_alpha()
    inverted_left = pygame.image.load('images/track_images/inverted_left_track.png').convert_alpha()
    start_train_station = pygame.image.load('images/track_images/start_train_station.png').convert_alpha()
    end_train_station = pygame.image.load('images/track_images/end_train_station.png').convert_alpha()

class TerrainSprites: # temp sprites, change out
    grass = pygame.image.load('images/tile_assets/grass_tiles/grass.png').convert_alpha()
    tallgrass = pygame.image.load('images/tile_assets/grass_tiles/tallgrass.png').convert_alpha()
    water = pygame.image.load('images/placeholders/blue.png').convert_alpha()
    ice = pygame.image.load('images/tile_assets/ice_tiles/Ice.png').convert_alpha()
    snow = pygame.image.load('images/tile_assets/snow_tiles/Snow_1.png').convert_alpha()

class ObstacleSprites:
    rock = pygame.image.load('images/obstacle_images/rock.png').convert_alpha()
    sandrock = pygame.image.load('images/obstacle_images/sandrock.png').convert_alpha()
    sadrock = pygame.image.load('images/obstacle_images/sadrock.png').convert_alpha()
    tree = pygame.image.load('images/obstacle_images/tree.png').convert_alpha()
    woodshack = pygame.image.load('images/obstacle_images/woodshack.png').convert_alpha()

class EventSprites:
    snowflake_icon = pygame.image.load('images/event_images/snowflake_icon.png').convert_alpha()

class TrainSprites:
    red_train = pygame.image.load('images/train_images/red_train.png').convert_alpha()
    gray_cargo = pygame.image.load('images/train_images/gray_cargo.png').convert_alpha()
    red_cargo = pygame.image.load('images/train_images/red_cargo.png').convert_alpha()
    blue_cargo = pygame.image.load('images/train_images/blue_cargo.png').convert_alpha()
    rock_cargo = pygame.image.load('images/train_images/old_train_images/rock_cargo.png').convert_alpha()
    propane_cargo = pygame.image.load('images/train_images/nuclear_cargo.png').convert_alpha()
    random_train_choice = ([red_train, gray_cargo, red_cargo, blue_cargo, rock_cargo, propane_cargo])

class PowerupSprites:
    bomb = pygame.image.load('images/powerup_images/bomb.png').convert_alpha()
    bomb_lit = pygame.image.load('images/powerup_images/bomb_lit.png').convert_alpha()
    explosion_images = [
        pygame.image.load('images/powerup_images/bomb1.png'),
        pygame.image.load('images/powerup_images/bomb2.png'),
        pygame.image.load('images/powerup_images/bomb3.png'),
        pygame.image.load('images/powerup_images/bomb4.png'),
        pygame.image.load('images/powerup_images/bomb5.png'),
        pygame.image.load('images/powerup_images/bomb6.png'),
        pygame.image.load('images/powerup_images/bomb7.png'),
        pygame.image.load('images/powerup_images/bomb8.png'),
        pygame.image.load('images/powerup_images/bomb9.png')
    ]

class Colors:
    black = (0, 0, 0)
    white = (255, 255, 255)
    dark_gray = (40, 40, 40)
    light_gray = (70,70,70)
    red = (255, 0, 0)
    sky_blue = (202, 228, 241)
    green = (0, 255, 0)