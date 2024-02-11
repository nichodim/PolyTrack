# Creators: Neo Chen, Matthew Selvaggi, Nicholas Seagal, Kelvin Huang
# Game Description: ...
import pygame
import sys
import random


# Constant variables - things you would configure
# Resolution config
GAME_WIDTH = 1000
GAME_HEIGHT = 1100

# Board config
OUTER_BORDER_SIZE = 150
NUM_ROWS = 10
NUM_COLS = 10
INNER_GAP = 10
OUTER_GAP = 35

# Trackbox config
TRACK_WIDTH = 50
TRACK_HEIGHT = 50
NUMBER_OF_TRACKS = 5
TRACK_SEPERATION = 100

# Initialize the pygame settings
pygame.init()
game_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT)) # Viewport Size
fps = pygame.time.Clock() # Games FPS

# Class to define colors that will be later called
class Colors:
    black = (0, 0, 0)
    white = (255, 255, 255)
    dark_gray = (40, 40, 40)
    light_gray = (70,70,70)


# Creates a board rectangle where tiles will be placed
board_width = NUM_COLS * TRACK_WIDTH + INNER_GAP * (NUM_COLS - 1) + OUTER_GAP * 2
board_height = NUM_ROWS * TRACK_HEIGHT + INNER_GAP * (NUM_ROWS - 1) + OUTER_GAP * 2
board_x = GAME_WIDTH / 2 - board_width / 2
board = pygame.Rect(board_x, GAME_HEIGHT * 0.1, board_width, board_height)

# Creates a 2d list with all of the tiles
# All tiles are preset with their correct position respective to the board
# Each tile is a list with 2 values
#       - The board rectangle itself
#       - The track rectangle that may attach to it
grid_tiles = []
row_y_increment = TRACK_HEIGHT + INNER_GAP
row_y = board.top + OUTER_GAP
for row in range(NUM_ROWS):  
    tile_x = OUTER_GAP

    row_list = []
    for col in range(NUM_COLS): 
        board_tile = pygame.Rect(board.left + tile_x, row_y, TRACK_WIDTH, TRACK_HEIGHT)
        row_list.append({"board": board_tile, "track": None})

        tile_x += TRACK_WIDTH + INNER_GAP
    grid_tiles.append(row_list)    

    row_y += row_y_increment 


# Creates the boxes to drag and drop
extra_width = TRACK_WIDTH * 0.75
extra_height = TRACK_WIDTH / 2

# Creates track box underneath the tracks
track_box_width = NUMBER_OF_TRACKS * TRACK_WIDTH + (TRACK_SEPERATION - TRACK_WIDTH) * (NUMBER_OF_TRACKS - 1) + extra_width * 4
track_box_x = GAME_WIDTH / 2 - track_box_width / 2
track_box = pygame.Rect(track_box_x, GAME_HEIGHT * 0.85, track_box_width, TRACK_HEIGHT + extra_height * 2)

# Creates tracks respective to the toolbox
active_track = None
tracks = []
track_x = extra_width * 2
for i in range(NUMBER_OF_TRACKS): 
    y = GAME_HEIGHT * 0.85
    track = pygame.Rect(track_box.left + track_x, track_box.center[1] - extra_height, TRACK_WIDTH, TRACK_HEIGHT)
    track_x += TRACK_SEPERATION
    tracks.append(track)
    
      

# Pygame mainloop that will run while the game is running
while True:
    for event in pygame.event.get(): 

        if event.type == pygame.MOUSEBUTTONDOWN: # Checks for left mouse button clicks on boxes
            if event.button == 1:
                for num, track in enumerate(tracks):
                    if track.collidepoint(event.pos):
                        # Check if track is attached 
                        for i, row in enumerate(grid_tiles):
                            for j, tile in enumerate(row):
                                if tile['track'] == tracks[num]:
                                    grid_tiles[i][j]['track'] = None

                        active_track = num
        
        if event.type == pygame.MOUSEBUTTONUP: # Checks for left mouse button releases on boxes
            if event.button == 1:
                # Check if pointer over an empty board tile
                #   -> Snap track to board tile and link track to tile
                for i, row in enumerate(grid_tiles):
                    for j, tile in enumerate(row):
                        if tile['board'].collidepoint(event.pos) and not grid_tiles[i][j]['track']:
                            tracks[active_track].x = grid_tiles[i][j]['board'].left
                            tracks[active_track].y = grid_tiles[i][j]['board'].top
                            grid_tiles[i][j]['track'] = tracks[active_track]

                active_track = None
        
        if event.type == pygame.MOUSEMOTION: # Moves box according to mouse movement
            if active_track != None:
                tracks[active_track].move_ip(event.rel)

        if event.type == pygame.QUIT: # Quits game if event is told to quit
            pygame.quit()
            sys.exit()

    # Fills background black
    game_surf.fill(Colors.dark_gray)

    # draws the board and tiles on screen
    pygame.draw.rect(game_surf, Colors.light_gray, board)
    for row in grid_tiles:
        for tile in row:
            pygame.draw.rect(game_surf, "white", tile['board'])

    pygame.draw.rect(game_surf, "black", track_box)
    # Draws the tracks on the screen
    for track in tracks:
        pygame.draw.rect(game_surf, "red", track)


    # Updates the display with previous functions
    pygame.display.update()
 
                                
    # Sets games FPS to 60
    fps.tick(60)
