import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (107, 186, 33)

BODY_SIZE = 20
MOVEMENT = 20
ANIMATION_SPEED = 3

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


def calculate_apple_coordinates(maximum, segment_size):
    coords = []
    co = 0
    i = 0

    while co < maximum:
        co = segment_size * i
        coords.append(co)
        i += 1

    return coords


class Game:

    def __init__(self, display_surface, worm):
        self.display_surface = display_surface
        self.direction = DOWN

        self.canvas_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.worm = worm
        self.worm.add()
        self.worm.add()

        self.x_coordinates = calculate_apple_coordinates(SCREEN_WIDTH - BODY_SIZE, BODY_SIZE)
        self.y_coordinates = calculate_apple_coordinates(SCREEN_HEIGHT - BODY_SIZE, BODY_SIZE)

        self.apples = []
        self.add_apple()

        self.score_inc = 20
        self.score_font = pygame.font.SysFont("comicsansms", 20)
        self.apples_consumed = 0

    def draw(self):
        # draw the background
        self.display_surface.fill(WHITE)

        # draw the worm
        for b in self.worm.body:
            pygame.draw.rect(self.display_surface, GREEN, b.rect)

        # draw any apples
        for a in self.apples:
            pygame.draw.rect(self.display_surface, RED, a.rect)

        self.display_surface.blit(self.get_score_label(), (10, 5))

    def get_score_label(self):
        return self.score_font.render("Score: " + str(self.apples_consumed * self.score_inc), True, BLACK)

    def animate(self):
        self.worm.move()

    def update_direction(self, event):
        if event.key == pygame.K_LEFT and self.worm.current_direction is not RIGHT:
            self.worm.current_direction = LEFT
        if event.key == pygame.K_RIGHT and self.worm.current_direction is not LEFT:
            self.worm.current_direction = RIGHT
        if event.key == pygame.K_UP and self.worm.current_direction is not DOWN:
            self.worm.current_direction = UP
        if event.key == pygame.K_DOWN and self.worm.current_direction is not UP:
            self.worm.current_direction = DOWN

    def check_collisions(self):
        head = self.worm.head
        body = self.worm.body[1:]

        # First check for a boundary collision with the appropriate edge of the playing area
        if self.direction == UP:
            p = head.rect.midtop
        elif self.direction == DOWN:
            p = head.rect.midbottom
        elif self.direction == LEFT:
            p = head.rect.midleft
        else:
            p = head.rect.midright

        """ pygame.Rect.collidepoint: A point along the right or bottom edge is not considered to be inside the rectangle
        To get around this inflate the canvas rect by 2 and use this to check for the collision. This allows the worm
        to get right up to the edges without ending the game prematurely """
        if not self.canvas_rect.inflate(2, 2).collidepoint(p):
            return True

        # Next check that the head is not colliding with any part of the body
        if head.rect.collidelistall(body):
            return True

        return False

    def add_apple(self):
        coord = None
        found = False

        while not found:
            coord = self.generate_apple_coordinate()
            r = pygame.Rect(coord[0], coord[1], BODY_SIZE, BODY_SIZE)

            if r.collidelist(self.worm.body):
                found = True

        self.apples.append(Apple(coord))

    def check_apple_eaten(self):
        for i in range(len(self.apples)):
            if self.worm.head.rect.colliderect(self.apples[i]):
                self.apples_consumed += 1
                del self.apples[i]
                self.add_apple()
                return True
        return False

    def generate_apple_coordinate(self):
        i = random.randint(1, len(self.x_coordinates) - 1)
        j = random.randint(1, len(self.y_coordinates) - 1)

        coord = (self.x_coordinates[i], self.y_coordinates[j])
        print(coord)
        return coord


class Worm:
    length = None
    body = []
    current_direction = None

    def __init__(self, start_x, start_y):
        self.length = 1
        self.ani_speed = ANIMATION_SPEED
        self.body.append(BodySegment(start_x, start_y, DOWN))
        self.current_direction = DOWN
        self.head = self.body[0]

    def add(self):
        last = self.body[-1]

        if last.direction == UP:
            new_x = last.rect.x
            new_y = last.rect.y + BODY_SIZE
        elif last.direction == DOWN:
            new_x = last.rect.x
            new_y = last.rect.y - BODY_SIZE
        elif last.direction == LEFT:
            new_x = last.rect.x - BODY_SIZE
            new_y = last.rect.y
        else:
            new_x = last.rect.x + BODY_SIZE
            new_y = last.rect.y

        # reset the animation speed to 0 to make the newly added segment appear instantly.
        self.ani_speed = 0
        self.body.append(BodySegment(new_x, new_y, last.direction))

    def move(self):
        if self.ani_speed > 0:
            self.ani_speed -= 1
            return

        old_head = self.head

        if self.current_direction == UP:
            new_x = old_head.rect.x
            new_y = old_head.rect.y - MOVEMENT
        elif self.current_direction == DOWN:
            new_x = old_head.rect.x
            new_y = old_head.rect.y + MOVEMENT
        elif self.current_direction == LEFT:
            new_x = old_head.rect.x - MOVEMENT
            new_y = old_head.rect.y
        else:
            new_x = old_head.rect.x + MOVEMENT
            new_y = old_head.rect.y

        self.body.pop()
        new_head = BodySegment(new_x, new_y, self.current_direction)
        self.body.insert(0, new_head)
        self.head = new_head

        self.ani_speed = ANIMATION_SPEED


class BodySegment:
    x_co = None
    y_co = None
    size = None
    rect = None
    direction = None

    def __init__(self, x_co, y_co, direction):
        self.x_co = x_co
        self.y_co = y_co
        self.size = BODY_SIZE
        self.direction = direction
        self.rect = pygame.Rect(self.x_co, self.y_co, self.size, self.size)

    def xy(self):
        return pygame.Rect(self.x_co, self.y_co, 2, 2)

    def __str__(self):
        return "x = " + str(self.x_co) + ", y = " + str(self.y_co)


class Apple:
    x_co = None
    y_co = None

    def __init__(self, coordinate):
        self.x_co = coordinate[0]
        self.y_co = coordinate[1]

        self.rect = pygame.Rect(self.x_co, self.y_co, BODY_SIZE, BODY_SIZE)
