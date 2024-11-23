import pygame
import random
import time
from enum import Enum
from stack import Stack

# display constant
UNIT: int = 21
WIDTH: int = 40
HEIGHT = 40

SCREEN_WIDTH: int = WIDTH * UNIT
SCREEN_HEIGHT: int = HEIGHT * UNIT

# color constant
DEEP_GREY: tuple[int, int, int] = (40, 40, 40)
LIGHT_GREY: tuple[int, int, int] = (60, 60, 60)
WHITE: tuple[int, int, int] = (255, 255, 255)
RED: tuple[int, int, int] = (255, 0, 0)
GREEN = (0, 255, 0)

# direction constant
UP = [0, -1]
DOWN = [0, 1]
LEFT = [-1, 0]
RIGHT = [1, 0]

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

MOVE_COMMAND_KEYS: set = {pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d}

# start point
X_START: int = 4
Y_START: int = 4

# interval time
INTERVAL_TIME: float = 0.1

# maximum path cost constant
INF: int = WIDTH * HEIGHT * 2 + 1


# direction enum class
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Node:
    def __init__(self, cost: int, direction: Direction):
        self.cost: int = cost
        self.parent_direction: Direction = direction


class Snake:
    def __init__(self):
        pygame.init()

        # set screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")

        # set snake body
        self.snake_body: list[list[int]] = [[X_START, Y_START]]

        # set apple position
        self.apple: list[int] = [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]
        while self.apple in self.snake_body:
            self.apple = [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]

        # set move direction
        self.move_direction = Direction.RIGHT

        self.last_move_time = time.time()

        self.is_game_finish = False

    def auto_play(self):
        while True:
            self.background_render()
            self.apple_render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.find_best_path()
            self.move()
            self.snake_body_render()
            if self.is_game_finish:
                time.sleep(1)
                self.refresh()
                continue
            while time.time() - self.last_move_time < INTERVAL_TIME:
                continue
            self.last_move_time = time.time()
            pygame.display.update()

    def find_best_path(self):
        distance_to_apple = \
            [[Node(INF, Direction.RIGHT) for _ in range(HEIGHT)] for _ in range(WIDTH)]
        distance_to_tail = \
            [[Node(INF, Direction.RIGHT) for _ in range(HEIGHT)] for _ in range(WIDTH)]

        apple_reachable: list[list[bool]] = [[True for _ in range(HEIGHT)] for _ in range(WIDTH)]
        tail_reachable: list[list[bool]] = [[True for _ in range(HEIGHT)] for _ in range(WIDTH)]

        for i in range(1, len(self.snake_body)):
            apple_reachable[self.snake_body[i][0]][self.snake_body[i][1]] = False
            tail_reachable[self.snake_body[i][0]][self.snake_body[i][1]] = False

        if self.direct_move(apple_reachable):
            return

        self.bfs(self.apple, distance_to_apple, apple_reachable)
        self.bfs(self.snake_body[-1], distance_to_tail, tail_reachable)

        if distance_to_apple[self.snake_body[0][0]][self.snake_body[0][1]].cost < INF:
            self.move_direction = (
                distance_to_apple[self.snake_body[0][0]][self.snake_body[0][1]].parent_direction)

        elif distance_to_tail[self.snake_body[0][0]][self.snake_body[0][1]].cost < INF:
            self.move_direction = (
                distance_to_tail[self.snake_body[0][0]][self.snake_body[0][1]].parent_direction)
        else:
            x_deepest, y_deepest = self.deepest_point()
            if x_deepest == self.snake_body[0][0] and y_deepest == self.snake_body[0][1]:
                self.wander()
            distance_to_deep = \
                [[Node(INF, Direction.RIGHT) for _ in range(HEIGHT)] for _ in range(WIDTH)]
            deep_reachable: list[list[bool]] = \
                [[True for _ in range(HEIGHT)] for _ in range(WIDTH)]
            for i in range(1, len(self.snake_body)):
                deep_reachable[self.snake_body[i][0]][self.snake_body[i][1]] = False
            for i in range(0, WIDTH):
                deep_reachable[i][0] = False
                deep_reachable[i][HEIGHT - 1] = False
            for j in range(0, HEIGHT):
                deep_reachable[0][j] = False
                deep_reachable[WIDTH - 1][j] = False

            self.bfs(self.snake_body[0], distance_to_deep, deep_reachable)
            self.move_direction = (
                distance_to_tail[self.snake_body[0][0]][self.snake_body[0][1]].parent_direction)

    def direct_move(self, apple_reachable) -> bool:
        x_step = 1 if self.apple[0] >= self.snake_body[0][0] else -1
        y_step = 1 if self.apple[1] >= self.snake_body[0][1] else -1

        x_head = self.snake_body[0][0]
        y_head = self.snake_body[0][1]

        can_vertical_move: bool = True
        can_horizontal_move: bool = True

        if x_head != self.apple[0]:
            while x_head != self.apple[0]:
                if not apple_reachable[x_head][y_head]:
                    can_horizontal_move = False
                    break
                x_head += x_step

            while y_head != self.apple[1]:
                if not apple_reachable[x_head][y_head]:
                    can_vertical_move = False
                    break
                y_head += y_step

            if can_vertical_move and can_horizontal_move:
                if x_step == 1:
                    self.move_direction = Direction.RIGHT
                else:
                    self.move_direction = Direction.LEFT
                return True

        x_head = self.snake_body[0][0]
        y_head = self.snake_body[0][1]

        can_vertical_move: bool = True
        can_horizontal_move: bool = True

        if y_head != self.apple[1]:
            while y_head != self.apple[1]:
                if not apple_reachable[x_head][y_head]:
                    can_vertical_move = False
                    break
                y_head += y_step

            while x_head != self.apple[0]:
                if not apple_reachable[x_head][y_head]:
                    can_horizontal_move = False
                    break
                x_head += x_step

            if can_vertical_move and can_horizontal_move:
                if y_step == 1:
                    self.move_direction = Direction.DOWN
                else:
                    self.move_direction = Direction.UP
                return True

        return False

    def deepest_point(self) -> tuple[int, int]:
        distance_to_head = \
            [[Node(INF, Direction.RIGHT) for _ in range(HEIGHT)] for _ in range(WIDTH)]
        head_reachable: list[list[bool]] = \
            [[True for _ in range(HEIGHT)] for _ in range(WIDTH)]
        for i in range(1, len(self.snake_body)):
            head_reachable[self.snake_body[i][0]][self.snake_body[i][1]] = False
        for i in range(0, WIDTH):
            head_reachable[i][0] = False
            head_reachable[i][HEIGHT - 1] = False
        for j in range(0, HEIGHT):
            head_reachable[0][j] = False
            head_reachable[WIDTH - 1][j] = False
        self.bfs(self.snake_body[0], distance_to_head, head_reachable)
        max_distance = 0
        x_max, y_max = self.snake_body[0][0], self.snake_body[0][1]
        for i in range(0, WIDTH):
            for j in range(0, HEIGHT):
                if not head_reachable[i][j]:
                    continue
                if distance_to_head[i][j].cost > max_distance:
                    max_distance = distance_to_head[i][j].cost
                    x_max, y_max = i, j
        return x_max, y_max

    def wander(self):
        random_direction = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        self.move_direction = random.choice(random_direction)

    @classmethod
    def bfs(cls, start_point: list[int], rec: list[list[Node]],
            reachable: list[list[bool]]):
        rec[start_point[0]][start_point[1]].cost = 0
        stk = Stack()
        stk.push(start_point)
        while not stk.is_empty():
            cur_point = stk.pop()
            reachable[cur_point[0]][cur_point[1]] = False
            for direction in DIRECTIONS:
                next_point = [cur_point[0] + direction[0], cur_point[1] + direction[1]]
                if next_point[0] < 0 or next_point[0] >= WIDTH:
                    continue
                elif next_point[1] < 0 or next_point[1] >= HEIGHT:
                    continue
                if not reachable[next_point[0]][next_point[1]]:
                    continue
                val1 = rec[next_point[0]][next_point[1]].cost
                val2 = rec[cur_point[0]][cur_point[1]].cost + 1
                cur_cost = min(val1, val2)
                if cur_cost < rec[next_point[0]][next_point[1]].cost:
                    rec[next_point[0]][next_point[1]].cost = cur_cost
                    if direction == UP:
                        rec[next_point[0]][next_point[1]].parent_direction = Direction.DOWN
                    elif direction == DOWN:
                        rec[next_point[0]][next_point[1]].parent_direction = Direction.UP
                    elif direction == LEFT:
                        rec[next_point[0]][next_point[1]].parent_direction = Direction.RIGHT
                    elif direction == RIGHT:
                        rec[next_point[0]][next_point[1]].parent_direction = Direction.LEFT
                stk.push(next_point)

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
            while time.time() - self.last_move_time < INTERVAL_TIME:
                continue
            self.last_move_time = time.time()
            pygame.display.update()

    def refresh(self):
        self.snake_body.clear()
        self.snake_body.append([X_START, Y_START])

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
        for i in range(len(self.snake_body)):
            rect_x = self.snake_body[i][0] * UNIT
            rect_y = self.snake_body[i][1] * UNIT
            rect = pygame.Rect(rect_x, rect_y, UNIT, UNIT)
            if i == 0:
                pygame.draw.rect(self.screen, GREEN, rect)
            else:
                pygame.draw.rect(self.screen, WHITE, rect)
                x_start = self.snake_body[i][0] * UNIT + UNIT // 2
                y_start = self.snake_body[i][1] * UNIT + UNIT // 2
                x_end = self.snake_body[i - 1][0] * UNIT + UNIT // 2
                y_end = self.snake_body[i - 1][1] * UNIT + UNIT // 2
                pygame.draw.line(self.screen, GREEN,
                                 (x_start, y_start), (x_end, y_end), 5)

    def apple_render(self):
        rect_x = self.apple[0] * UNIT
        rect_y = self.apple[1] * UNIT
        rect = pygame.Rect(rect_x, rect_y, UNIT, UNIT)
        pygame.draw.rect(self.screen, RED, rect)
