# Top level of the game, responsible for states such as scenes and menus

import pygame
from button import Button
from game import Game
from constants import *
import maps
import sys


pygame.init()
pygame.mixer.music.load(SFX.theme_song)
pygame.mixer.music.set_volume(0.015)
pygame.mixer.music.play(-1)

def main():
    # Initialize main
    pygame.init()
    game = Game(maps.VanillaMap) # TODO make this choosable in menu

    # Set buttons
    image_scale = 6
    button_x = GAME_WIDTH / 2 - (Images.start_img.get_width() * image_scale / 2)
    start_button = Button(button_x, 400, Images.start_img, image_scale)
    quit_button = Button(button_x, 500, Images.quit_img, image_scale)
    grass_map = Button(400, 400, Images.grass_map, image_scale)
    snow_map = Button(900, 400, Images.snow_map, image_scale)

    # Set title
    image_scale = 2
    title_image_width, title_image_height = Images.title_img.get_size()
    title_button_x = (GAME_WIDTH - title_image_width * image_scale) / 2
    title_button_y = (GAME_HEIGHT - title_image_height * image_scale) / 2 - 170
    title_button = Button(title_button_x, title_button_y, Images.title_img, image_scale)

    run = True
    while run:
        # Draw menu
        main_surf.fill(Colors.sky_blue)
        start_button.draw(main_surf)
        quit_button.draw(main_surf)
        title_button.draw(main_surf)
        
        # Check buttons
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.clicked():
                    map_menu()
                if quit_button.clicked():
                    run = False
        
        # Set start button to track when hovered
        if start_button.hovered():
            start_button.setImage(Images.start_hover_img)
        else:
            start_button.setImage(Images.start_img)

        if quit_button.hovered():
            quit_button.setImage(Images.quit_hover_img)
        else:
            quit_button.setImage(Images.quit_img)

        # Check for end event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()        
    pygame.mixer.music.stop()

def map_menu():  # Give it its own file at a later date
    pygame.init()

    image_scale = 3
    button_x = GAME_WIDTH / 4
    button_radius = Images.grass_map.get_width() * 3 / 2
    map_button_radius = Images.mapmenu_img.get_width() * 2 / 2
    grass_map = Button(button_x - button_radius, 400, Images.grass_map, image_scale)
    snow_map = Button(2 * button_x - button_radius, 400, Images.snow_map, image_scale)
    snow_mapL = Button(3 * button_x - button_radius, 400, Images.snow_map_large, image_scale)
    map_img = Button(2 * button_x - map_button_radius, 100, Images.mapmenu_img, 2)
    

    run = True
    while run:
        main_surf.fill(Colors.sky_blue)
        grass_map.draw(main_surf)
        snow_map.draw(main_surf)
        snow_mapL.draw(main_surf)
        map_img.draw(main_surf)
        

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if grass_map.clicked():
                    game = Game(maps.VanillaMap)
                    game.run()
                if snow_map.clicked():
                    game = Game(maps.SnowMap)
                    game.run()
                if snow_mapL.clicked():
                    game = Game(maps.SnowMapL)
                    game.run()
                
        


        pygame.display.update() 

def quit():
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()