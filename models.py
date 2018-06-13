import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SEGMENT_SIZE = 20
MOVEMENT = 20
ANIMATION_SPEED = 10

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
            return not self.rect.collidepoint(head.rect.midleft)
        else:
            return not self.rect.collidepoint(head.rect.midright)


class Snake:
    length = None
    body = []
    direction = UP

    def __init__(self, start_x, start_y):
        self.length = 1
        self.body.append(BodySegment(start_x, start_y))
        self.ani_speed = ANIMATION_SPEED

        self.add()
        self.add()

    def draw(self, surface):
        head = True
        for segment in self.body:
            if head:
                pygame.draw.rect(surface, GREEN, segment.rect)
                head = False
            else:
                pygame.draw.rect(surface, RED, segment.rect)
                pygame.draw.rect(surface, BLACK, segment.xy())

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

        print("current x", last.x_co, "current y", last.y_co)
        print("new x", new_x, "new y", new_y)
        self.body.append(BodySegment(new_x, new_y))

    def move(self):
        if self.ani_speed > 0:
            self.ani_speed -= 1
            return

        old_head = self.body[0]

        if self.direction == UP:
            new_x = old_head.rect.x
            new_y = old_head.rect.y - MOVEMENT
        elif self.direction == DOWN:
            new_x = old_head.rect.x
            new_y = old_head.rect.y + MOVEMENT
        elif self.direction == LEFT:
            new_x = old_head.rect.x - MOVEMENT
            new_y = old_head.rect.y
        else:
            new_x = old_head.rect.x + MOVEMENT
            new_y = old_head.rect.y

        self.body.pop()
        new_head = BodySegment(new_x, new_y)
        self.body.insert(0, new_head)

        self.ani_speed = ANIMATION_SPEED

    def update_direction(self, event):
        if event.key == pygame.K_LEFT and self.direction is not RIGHT:
            self.direction = LEFT
        if event.key == pygame.K_RIGHT and self.direction is not LEFT:
            self.direction = RIGHT
        if event.key == pygame.K_UP and self.direction is not DOWN:
            self.direction = UP
        if event.key == pygame.K_DOWN and self.direction is not UP:
            self.direction = DOWN


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

    def xy(self):
        return pygame.Rect(self.x_co, self.y_co, 2, 2)

    def __str__(self):
        return "x = " + self.x_co + ", y = " + self.y_co
