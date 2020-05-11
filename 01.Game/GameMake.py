# Pygame　ゲーム作成
import pygame
from pygame.locals import *
import sys
import random
import copy

window_size = 640, 480

def main():
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("TEST")

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()