import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SEGMENT_SIZE = 40
MOVEMENT = 2

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


class Snake:
    length = None
    body = []
    direction = RIGHT

    def __init__(self, start_x, start_y):
        self.length = 1
        self.body.append(BodySegment(start_x, start_y))

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, segment.rect)
            pygame.draw.rect(surface, BLACK, pygame.Rect(segment.x_co, segment.y_co, 2, 2))

    def add(self):
        last = self.body[-1]
        if self.direction == UP:
            self.body.append(BodySegment(last.rect.bottomright[0], last.rect.bottom + 1))
        elif self.direction == RIGHT:
            self.body.append(BodySegment(last.rect.x + SEGMENT_SIZE + 2, last.rect.y))

    def move(self):
        for segment in self.body:
            segment.update(self.direction)


class BodySegment:
    x_co = None
    y_co = None
    size = None
    rect = None

    def __init__(self, x_co, y_co):
        self.x_co = x_co
        self.y_co = y_co
        self.size = SEGMENT_SIZE
        self.rect = pygame.Rect(self.x_co, self.y_co, self.size, self.size)

    def update(self, direction):
        if direction == UP:
            self.y_co -= MOVEMENT
        elif direction == DOWN:
            self.y_co += MOVEMENT
        elif direction == LEFT:
            self.x_co += MOVEMENT
        else:
            self.x_co -= MOVEMENT

        self.rect = pygame.Rect(self.x_co, self.y_co, self.size, self.size)
