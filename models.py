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


class Canvas:
    size = None

    def __init__(self, size):
        self.size = size
        self.rect = pygame.Rect(0, 0, self.size, self.size)

    def boundary_collision(self, snake):
        head = snake.body[0]
        dir = snake.direction

        if dir == UP:
            return not self.rect.collidepoint(head.rect.midtop)
        if dir == DOWN:
            return not self.rect.collidepoint(head.rect.midbottom)
        elif dir == LEFT:
            return not self.rect.collidepoint(head.rect.midlieft)
        else:
            return not self.rect.collidepoint(head.rect.midright)


class Snake:
    length = None
    body = []
    direction = DOWN

    def __init__(self, start_x, start_y):
        self.length = 1
        self.body.append(BodySegment(start_x, start_y))

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, segment.rect)
            pygame.draw.rect(surface, BLACK, pygame.Rect(segment.x_co, segment.y_co, 2, 2))

    def add(self):
        last = self.body[-1]
        new_x = None
        new_y = None

        if self.direction == UP:
            new_x = last.rect.x
            new_y = last.rect.y + SEGMENT_SIZE
        elif self.direction == DOWN:
            new_x = last.rect.x
            new_y = last.rect.y - SEGMENT_SIZE
        elif self.direction == LEFT:
            new_x = last.rect.x - SEGMENT_SIZE
            new_y = last.rect.y
        else:
            new_x = last.rect.x + SEGMENT_SIZE
            new_y = last.rect.y

        self.body.append(BodySegment(new_x, new_y))

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
            self.x_co -= MOVEMENT
        else:
            self.x_co += MOVEMENT

        self.rect = pygame.Rect(self.x_co, self.y_co, self.size, self.size)
