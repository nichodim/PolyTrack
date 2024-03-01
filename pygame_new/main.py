# Top level of the game, responsible for states such as scenes and menus

import pygame
from button import Button
from game import Game
from constants import *

main_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

def main():
    # Initialize main
    pygame.init()
    game = Game()

    # Set buttons
    image_scale = 3.5
    button_x = GAME_WIDTH / 2 - (Images.start_img.get_width() * image_scale / 2)
    start_button = Button(button_x, 400, Images.start_img, image_scale)
    quit_button = Button(button_x, 500, Images.quit_img, image_scale)
    
    run = True
    while run:
        # Draw menu
        main_surf.fill(Colors.sky_blue)
        start_button.draw(main_surf)
        quit_button.draw(main_surf)
        
        # Check buttons
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.clicked():
                    game.run()
                if quit_button.clicked():
                    run = False
        
        # Set start button to track when hovered
        if start_button.hovered():
            start_button.setImage(Images.start_hover_img)
        else:
            start_button.setImage(Images.start_img)
        
        # Check for end event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
    
if __name__ == "__main__":
    main()