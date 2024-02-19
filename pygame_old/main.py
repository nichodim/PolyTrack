# Creators: Neo Chen, Matthew Selvaggi, Nicholas Seagal, Kelvin Huang
# Game Description: ...
import pygame
import sys
import random
import math

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
NUMBER_OF_TRACKS = 0
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

class Tracks:
    horizontal_track = pygame.image.load('images/horizontal_track.png') 
    straight_track = pygame.image.load('images/straight_track.png')
    right_track = pygame.image.load('images/right_track.png')
    left_track = pygame.image.load('images/left_track.png')

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
track_box_width = 5 * TRACK_WIDTH + (TRACK_SEPERATION - TRACK_WIDTH) * (5 - 1) + extra_width * 4
track_box_x = GAME_WIDTH / 2 - track_box_width / 2
track_box = pygame.Rect(track_box_x, GAME_HEIGHT * 0.85, track_box_width, TRACK_HEIGHT + extra_height * 2)

# Creates tracks respective to the toolbox
active_track = None
tracks = []
track_x = extra_width * 2

possible_tracks = [Tracks.horizontal_track, Tracks.straight_track, Tracks.left_track, Tracks.right_track]

time = 0

# Pygame mainloop that will run while the game is running
while True:
    for event in pygame.event.get(): 
        if event.type == pygame.MOUSEBUTTONDOWN: # Checks for left mouse button clicks on boxes
            if event.button == 1:

                for num, track in enumerate(tracks):
                    if track["track_location"].collidepoint(event.pos):

                        # Check if track is attached to the grid
                        for i, row in enumerate(grid_tiles):
                            for j, tile in enumerate(row):
                                if tile['track'] == tracks[num]:
                                    grid_tiles[i][j]['track'] = None
                        
                        active_track = num
        
        if event.type == pygame.MOUSEBUTTONUP: # Checks for left mouse button releases on boxes
            if event.button == 1 and active_track != None:

                # Check if pointer over an empty board tile
                #   -> Snap track to board tile and link track to tile

                # calculate the nearest row and column when tile is drop
                precice_row = ((event.pos[1] - board.top - OUTER_GAP) - 10 * ((event.pos[1] - board.top - OUTER_GAP) // 55)) // 50
                precice_column = ((event.pos[0] - board.left - OUTER_GAP) - 10 * ((event.pos[0] - board.left - OUTER_GAP) // 55)) // 50
    
                # first set of condition detects if it on the board 
                # second condition detects if the track is over a tile
                # third condition detects if the track is empty
                if (0 <= precice_row <= 9 and 0 <= precice_column<= 9) and grid_tiles[precice_row][precice_column]['board'].collidepoint(event.pos) and not grid_tiles[precice_row][precice_column]['track']:
                    tracks[active_track]["track_location"].x = grid_tiles[precice_row][precice_column]['board'].left
                    tracks[active_track]["track_location"].y = grid_tiles[precice_row][precice_column]['board'].top
                    grid_tiles[precice_row][precice_column]['track'] = tracks[active_track]

                    tracks.pop(active_track)
                    NUMBER_OF_TRACKS -= 1
                    for i in range(active_track, len(tracks)):
                        tracks[i]["track_location"].x -= TRACK_SEPERATION
                    
                # send the track back to it initial position if it fails to snap to the grid
                else:
                    tracks[active_track]["track_location"].x = track_box_x + extra_width * 2 + TRACK_SEPERATION * active_track
                    tracks[active_track]["track_location"].y = track_box.center[1] - extra_height
                
                active_track = None
        
        if event.type == pygame.MOUSEMOTION: # Moves box according to mouse movement
            if active_track != None:
                tracks[active_track]["track_location"].move_ip(event.rel)

        if event.type == pygame.QUIT: # Quits game if event is told to quit
            pygame.quit()
            sys.exit()
    
    time += 1
    if time % 60 == 0 and NUMBER_OF_TRACKS < 5:
        track = {    
                "track_location": pygame.Rect(track_box.left + extra_width * 2 + TRACK_SEPERATION * len(tracks), track_box.center[1] - extra_height, TRACK_WIDTH, TRACK_HEIGHT),
                "image": possible_tracks[random.randint(0, 3)]
            }

        print(track)

        #track_x += TRACK_SEPERATION
        NUMBER_OF_TRACKS += 1
        tracks.append(track)
    

    # Fills background black
    game_surf.fill(Colors.dark_gray)

    # draws the board and tiles on screen
    pygame.draw.rect(game_surf, Colors.light_gray, board)
    for row in grid_tiles:
        for tile in row:
            pygame.draw.rect(game_surf, "white", tile['board'])
            if tile['track'] != None:
                # Changes the scalling with the initalized sizes of the tile
                scaled_image_grid = pygame.transform.scale(tile['track']['image'], (TRACK_WIDTH, TRACK_HEIGHT))

                # Centers the the tracks by moving to origin (0,0)
                center = tile['track']['track_location'].move(0, 0)
                
                # Displays the images in
                game_surf.blit(scaled_image_grid, center)

    pygame.draw.rect(game_surf, "black", track_box)

   # Draws the tracks on the screen
    if len(tracks) > 0:
        for track in tracks:        
            # Scales the image to fit the preset track size of 50, 50
            scaled_image = pygame.transform.scale(track['image'], (TRACK_WIDTH, TRACK_HEIGHT))
            # Displays the images in the toolbox
            game_surf.blit(scaled_image, track['track_location'])
            
    # Updates the display with previous functions
    pygame.display.update()
 
                                
    # Sets games FPS to 60
    fps.tick(60)
