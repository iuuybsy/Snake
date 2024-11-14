import pygame
import random
import time
from enum import Enum

# display constant
UNIT: int = 20
WIDTH: int = 30
HEIGHT = 30

SCREEN_WIDTH: int = WIDTH * UNIT
SCREEN_HEIGHT: int = HEIGHT * UNIT

# color constant
DEEP_GREY: tuple[int, int, int] = (40, 40, 40)
LIGHT_GREY: tuple[int, int, int] = (60, 60, 60)
WHITE: tuple[int, int, int] = (255, 255, 255)
RED: tuple[int, int, int] = (255, 0, 0)

# direction constant
UP = [0, -1]
DOWN = [0, 1]
LEFT = [-1, 0]
RIGHT = [1, 0]

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

MOVE_COMMAND_KEYS: set = {pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d}


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Snake:
    def __init__(self):
        pygame.init()

        # set screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")

        # set snake body
        self.snake_body: list[list[int]] = [[14, 14]]

        # set apple position
        self.apple: list[int] = [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]
        while self.apple in self.snake_body:
            self.apple = [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]

        # set move direction
        self.move_direction = Direction.RIGHT

        # set move speed
        self.update_time: float = 0.1
        self.last_move_time = time.time()

        # game finish sign
        self.is_game_finish = False

    def play(self):
        while True:
            self.background_render()
            self.apple_render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        if self.move_direction == Direction.DOWN:
                            continue
                        elif self.move_direction == Direction.UP:
                            continue
                        self.move_direction = Direction.UP if event.key == pygame.K_w \
                            else Direction.DOWN
                    elif event.key == pygame.K_a or event.key == pygame.K_d:
                        if self.move_direction == Direction.LEFT:
                            continue
                        elif self.move_direction == Direction.RIGHT:
                            continue
                        self.move_direction = Direction.LEFT if event.key == pygame.K_a \
                            else Direction.RIGHT
            self.move()
            self.snake_body_render()
            if self.is_game_finish:
                time.sleep(1)
                self.refresh()
                continue
            while time.time() - self.last_move_time < self.update_time:
                continue
            self.last_move_time = time.time()
            pygame.display.update()

    def refresh(self):
        self.snake_body.clear()
        self.snake_body.append([14, 14])

        self.apple: list[int] = [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]
        while self.apple in self.snake_body:
            self.apple = [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]

        self.move_direction = Direction.RIGHT
        self.last_move_time = time.time()
        self.is_game_finish = False

    def move(self):
        dir_x = DIRECTIONS[self.move_direction.value][0]
        dit_y = DIRECTIONS[self.move_direction.value][1]
        tail_x = self.snake_body[-1][0]
        tail_y = self.snake_body[-1][1]
        for i in range(len(self.snake_body) - 1, 0, -1):
            self.snake_body[i][0] = self.snake_body[i - 1][0]
            self.snake_body[i][1] = self.snake_body[i - 1][1]
        self.snake_body[0][0] += dir_x
        self.snake_body[0][1] += dit_y

        if self.snake_body[0][0] < 0 or self.snake_body[0][0] >= WIDTH or \
                self.snake_body[0][1] < 0 or self.snake_body[0][1] >= HEIGHT:
            self.is_game_finish = True
            return
        elif len(self.snake_body) > 3:
            for i in range(1, len(self.snake_body)):
                if (self.snake_body[0][0] == self.snake_body[i][0] and
                        self.snake_body[0][1] == self.snake_body[i][1]):
                    self.is_game_finish = True
                    return
        if self.snake_body[0][0] == self.apple[0] and self.snake_body[0][1] == self.apple[1]:
            self.snake_body.append([tail_x, tail_y])
            self.apple = [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]
            while self.apple in self.snake_body:
                self.apple = [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]

    def background_render(self):
        for i in range(WIDTH):
            for j in range(HEIGHT):
                rect_x = i * UNIT
                rect_y = j * UNIT
                rect = pygame.Rect(rect_x, rect_y, UNIT, UNIT)
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.screen, LIGHT_GREY, rect)
                else:
                    pygame.draw.rect(self.screen, DEEP_GREY, rect)

    def snake_body_render(self):
        for body_part in self.snake_body:
            rect_x = body_part[0] * UNIT
            rect_y = body_part[1] * UNIT
            rect = pygame.Rect(rect_x, rect_y, UNIT, UNIT)
            pygame.draw.rect(self.screen, WHITE, rect)

    def apple_render(self):
        rect_x = self.apple[0] * UNIT
        rect_y = self.apple[1] * UNIT
        rect = pygame.Rect(rect_x, rect_y, UNIT, UNIT)
        pygame.draw.rect(self.screen, RED, rect)

