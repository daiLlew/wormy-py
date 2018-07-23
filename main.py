import sys

from pygame.locals import *

from models import *

FPS = 30


def main():
    pygame.init()
    global FPSCLOCK, DISPLAYSURF

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("Wormy-py")

    game = Game(DISPLAYSURF, Worm(400, 40))

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

        if game.check_collisions():
            running = False

        if game.check_apple_eaten():
            game.worm.add()

        game.animate()
        game.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()

