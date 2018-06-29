import sys

from pygame.locals import *

from models import *

WHITE = (255, 255, 255)
SCREEN_SIZE = 800
FPS = 30


def main():
    pygame.init()
    global FPSCLOCK, DISPLAYSURF


    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), 0, 32)
    pygame.display.set_caption("Wormy-py")

    game = Game(DISPLAYSURF, Worm(400, 40), SCREEN_SIZE)

    running = True

    while running:
        FPSCLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                print("exiting")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                game.update_direction(event)

        game.animate()

        if game.check_collisions():
            running = False

        game.check_apple_eaten()
        game.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
