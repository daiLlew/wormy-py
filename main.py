import sys
import pygame
from models import *
from pygame.locals import *

WHITE = (255, 255, 255)
SCREEN_SIZE = 800
FPS = 30


def main():
    pygame.init()
    global FPSCLOCK, DISPLAYSURF

    startPos = (SCREEN_SIZE / 2) - (SEGMENT_SIZE / 2)
    snake = Snake(startPos, startPos)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), 0, 32)
    pygame.display.set_caption("Hello world!")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                print("exiting")
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                snake.add()

        DISPLAYSURF.fill(WHITE)
        snake.draw(DISPLAYSURF)
        snake.move()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
