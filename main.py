import sys

from pygame.locals import *

from models import *

WHITE = (255, 255, 255)
SCREEN_SIZE = 800
FPS = 30


def main():
    pygame.init()
    global FPSCLOCK, DISPLAYSURF

    start_pos = (SCREEN_SIZE / 2) - (SEGMENT_SIZE / 2)
    snake = Snake(start_pos, start_pos)

    canvas = Canvas(SCREEN_SIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), 0, 32)
    pygame.display.set_caption("Wormy-py")

    running = True

    while running:
        FPSCLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                print("exiting")
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                snake.add()
            elif event.type == pygame.KEYDOWN:
                snake.update_direction(event)

        snake.move()

        DISPLAYSURF.fill(WHITE)
        snake.draw(DISPLAYSURF)

        if snake.check_collisions(canvas):
            running = False

        pygame.display.update()


if __name__ == '__main__':
    main()
