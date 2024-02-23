# Constants used throughout the game

import pygame

class Images:
    start_img = pygame.image.load('images/start.png')
    quit_img = pygame.image.load('images/quit.png')
class TrackSprites:
    horizontal_track = pygame.image.load('images/horizontal_track.png')
    straight_track = pygame.image.load('images/straight_track.png')
    right_track = pygame.image.load('images/right_track.png')
    left_track = pygame.image.load('images/left_track.png')
class Colors:
    black = (0, 0, 0)
    white = (255, 255, 255)
    dark_gray = (40, 40, 40)
    light_gray = (70,70,70)
    red = (255, 0, 0)
    sky_blue = (202, 228, 241)

# Constant variables - things you would configure
# Resolution config
GAME_WIDTH = 1000
GAME_HEIGHT = 700

# Board config
OUTER_BORDER_SIZE = 150
NUM_ROWS = 10
NUM_COLS = 10
INNER_GAP = 10
OUTER_GAP = 35

# Trackbox config
TRACK_WIDTH = 50
TRACK_HEIGHT = 50
TRACK_SEPERATION = TRACK_WIDTH * 2
EXTRA_WIDTH = TRACK_WIDTH * 0.75
EXTRA_HEIGHT = TRACK_HEIGHT / 2

NUMBER_OF_TRACKS = 0