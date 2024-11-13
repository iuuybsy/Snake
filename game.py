import pygame
import random

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


class Snake:
    def __init__(self):
        pygame.init()

        # set screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")

        # set snake body
        self.snake_body: list[list[int]] = [[14, 14]]

        # set apple position
        self.apple = [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]
        while self.apple in self.snake_body:
            self.apple = [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]

    def play(self):
        while True:
            self.background_render()
            self.snake_body_render()
            self.apple_render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            pygame.display.update()

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

