# Creators: Neo Chen, Matthew Selvaggi, Nicholas Seagal, Kelvin Huang
# Game Description: ...
import pygame
import sys

# Initialize the pygame settings
pygame.init()
game_view = pygame.display.set_mode((1000, 1000)) # Viewport Size
fps = pygame.time.Clock() # Games FPS

# Size of board
outer_border_size = 100
num_rows = 20
num_cols = 20

# Class to define colors that will be later called
class Colors:
    black = (0, 0, 0)
    white = (255, 255, 255)
    dark_gray = (40, 40, 40)
    light_gray = (70,70,70)

# Creates the list for row and col with inital val of 0
grid = []
for row in range(num_rows):                     # Row       # Col
    row_list = []               # i.e. grid = [[0,0,0,0], [0,0,0,0,] ...]
    for col in range(num_cols): 
        row_list.append(0)
    grid.append(row_list)      

# Pygame mainloop that will run while the game is running
while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # Quits game if event is told to quit
            pygame.quit()
            sys.exit()

    # Fills background black
    game_view.fill(Colors.dark_gray)
    
    # Overwrite the background to show a grid in the center of the viewport
    pygame.draw.rect(game_view, Colors.light_gray, (outer_border_size, outer_border_size, 1000 - 2 * outer_border_size, 1000 - 2 * outer_border_size))

    # Draws the lines in range of the viewport with a step of 50 to give grid size for x and y
    for x in range(0, 1000, 50):
        pygame.draw.line(game_view, Colors.dark_gray, (x, 0), (x, 1000))
    
    for y in range(0, 1000, 50):
        pygame.draw.line(game_view, Colors.dark_gray, (0, y), (1000, y))

    # Updates the display with previous functions
    pygame.display.update()
 
                                
    # Sets games FPS to 60
    fps.tick(60)
