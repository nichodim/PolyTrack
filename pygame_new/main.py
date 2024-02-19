# Top level of the game, responsible for states of the game
# Currently, the game only has the state of Game but could be menu and different scenes/levels

import pygame
from buttons import Button
from game import Game
from constants import GAME_WIDTH

screen = pygame.display.set_mode((GAME_WIDTH, 700))


        

def main():
    pygame.init()
    game = Game()
    start_button = Button(388, 400, start_img, 3.5)
    quit_button = Button(388, 500, quit_img, 3.5)
    
    run = True
    while run:
        screen.fill((202, 228, 241))
        
        if start_button.draw(screen):
            game.run_game()
        if quit_button.draw(screen):
            run = False
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    
    


if __name__ == "__main__":

    start_img = pygame.image.load('images/start.png').convert_alpha()
    quit_img = pygame.image.load('images/quit.png').convert_alpha()
    

    main()