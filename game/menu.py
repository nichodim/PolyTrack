from button import Button
from constants import *
from game import Game
import maps

# Modified Matthew Selvaggi
# Date:  5-21-24
# Purpose: Created the menu in its own file away from main, allows for more expansion later on.
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