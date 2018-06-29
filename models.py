import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SEGMENT_SIZE = 20
MOVEMENT = 20
ANIMATION_SPEED = 5

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


class Game:

    def __init__(self, display_surface, worm, size):
        self.display_surface = display_surface
        self.direction = DOWN

        self.size = size
        self.canvas_rect = pygame.Rect(0, 0, self.size, self.size)

        self.worm = worm
        self.worm.add(self.direction)
        self.worm.add(self.direction)

        self.apples = []
        self.apples.append(Apple())

    def draw(self):
        # draw the background
        self.display_surface.fill(WHITE)

        # draw the worm
        head = True
        for b in self.worm.body:
            if head:
                pygame.draw.rect(self.display_surface, GREEN, b.rect)
                head = False
            else:
                pygame.draw.rect(self.display_surface, RED, b.rect)
                pygame.draw.rect(self.display_surface, BLACK, b.xy())

        # draw any apples
        for a in self.apples:
            pygame.draw.rect(self.display_surface, BLACK, a.rect)

    def animate(self):
        self.worm.move(self.direction)

    def update_direction(self, event):
        if event.key == pygame.K_LEFT and self.direction is not RIGHT:
            self.direction = LEFT
        if event.key == pygame.K_RIGHT and self.direction is not LEFT:
            self.direction = RIGHT
        if event.key == pygame.K_UP and self.direction is not DOWN:
            self.direction = UP
        if event.key == pygame.K_DOWN and self.direction is not UP:
            self.direction = DOWN

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

        if not self.canvas_rect.collidepoint(p):
            return True

        # Next check that the head is not colliding with any part of the body
        if head.rect.collidelistall(body):
            return True

        return False

    def add_apple(self):
        self.apples.append(Apple())

    def check_apple_eaten(self):
        for i in range(len(self.apples)):
            if self.worm.head.rect.colliderect(self.apples[i]):
                print("apple consumed")
                self.worm.add(self.direction)
                del self.apples[i]
                break


class Worm:
    length = None
    body = []

    def __init__(self, start_x, start_y):
        self.length = 1
        self.ani_speed = ANIMATION_SPEED
        self.body.append(BodySegment(start_x, start_y))
        self.head = self.body[0]

    def add(self, direction):
        last = self.body[-1]

        if direction == UP:
            new_x = last.rect.x
            new_y = last.rect.y + SEGMENT_SIZE
        elif direction == DOWN:
            new_x = last.rect.x
            new_y = last.rect.y - SEGMENT_SIZE
        elif direction == LEFT:
            new_x = last.rect.x - SEGMENT_SIZE
            new_y = last.rect.y
        else:
            new_x = last.rect.x + SEGMENT_SIZE
            new_y = last.rect.y

        self.body.append(BodySegment(new_x, new_y))

    def move(self, direction):
        if self.ani_speed > 0:
            self.ani_speed -= 1
            return

        old_head = self.head

        if direction == UP:
            new_x = old_head.rect.x
            new_y = old_head.rect.y - MOVEMENT
        elif direction == DOWN:
            new_x = old_head.rect.x
            new_y = old_head.rect.y + MOVEMENT
        elif direction == LEFT:
            new_x = old_head.rect.x - MOVEMENT
            new_y = old_head.rect.y
        else:
            new_x = old_head.rect.x + MOVEMENT
            new_y = old_head.rect.y

        self.body.pop()
        new_head = BodySegment(new_x, new_y)
        self.body.insert(0, new_head)
        self.head = new_head

        self.ani_speed = ANIMATION_SPEED


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
        return "x = " + str(self.x_co) + ", y = " + str(self.y_co)


class Apple:
    x_co = None
    y_co = None

    def __init__(self):
        self.x_co = 120
        self.y_co = 120
        self.rect = pygame.Rect(self.x_co, self.y_co, SEGMENT_SIZE, SEGMENT_SIZE)

