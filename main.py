# author: Simon Heppner
# license: gpl, see LICENSE file
# idea: Based on the "Nautical" concept by Horst Jens and Simon Heppner (2020)

import pygame
from game_manager import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    """
    Main function to initialize and run the game.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Nautical")
    game = Game(screen)
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()
