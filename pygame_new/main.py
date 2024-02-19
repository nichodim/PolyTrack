# Top level of the game, responsible for states of the game
# Currently, the game only has the state of Game but could be menu and different scenes/levels

import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.run_game()

if __name__ == "__main__":
    main()