import pygame
from pygame.constants import (
    KEYDOWN,
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    QUIT)
from pygame.sprite import Sprite

pygame.init()

GRID_SIZE = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

POS_X_RANGE = SCREEN_WIDTH/GRID_SIZE
POS_Y_RANGE = SCREEN_HEIGHT/GRID_SIZE

NORTH = (0, -1 * GRID_SIZE)
SOUTH = (0, 1 * GRID_SIZE)
WEST = (-1 * GRID_SIZE, 0)
EAST = (1 * GRID_SIZE, 0)


class SnakeBody(Sprite):
    def __init__(self, index):
        super().__init__()
        self.surf = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.surf.fill((135, 206, 250))
        self.rect = self.surf.get_rect()
        self.rect.topleft = ((SCREEN_WIDTH)/2,
                             (SCREEN_HEIGHT/2 + index*GRID_SIZE))


class Snake():
    def __init__(self, length):
        super().__init__()
        self.body = []
        for i in range(length):
            body = SnakeBody(i)
            self.body.append(body)
        self.direction = NORTH

    def update(self, pressed_keys):
        if pressed_keys[K_UP] and self.direction != SOUTH:
            self.direction = NORTH
        if pressed_keys[K_DOWN] and self.direction != NORTH:
            self.direction = SOUTH
        if pressed_keys[K_LEFT] and self.direction != EAST:
            self.direction = WEST
        if pressed_keys[K_RIGHT] and self.direction != WEST:
            self.direction = EAST

        next_pos = self.body[0].rect.topleft
        for i in range(len(self.body)-1):
            tmp = self.body[i+1].rect.topleft
            self.body[i+1].rect.topleft = next_pos
            next_pos = tmp
        self.body[0].rect.move_ip(self.direction)
        if self.body[0].rect.top < 0:
            self.body[0].rect.top = 0
        if self.body[0].rect.left < 0:
            self.body[0].rect.left = 0
        if self.body[0].rect.right > SCREEN_WIDTH:
            self.body[0].rect.right = SCREEN_WIDTH
        if self.body[0].rect.bottom > SCREEN_HEIGHT:
            self.body[0].rect.bottom = SCREEN_HEIGHT


def draw_background(screen):
    COLOR_BACKGROUND = (0, 0, 0)
    COLOR_GRID = (200, 200, 200)
    screen.fill(COLOR_BACKGROUND)
    for x in range(GRID_SIZE, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(
            surface=screen,
            color=COLOR_GRID,
            start_pos=(0, x),
            end_pos=(SCREEN_WIDTH, x),
            width=1
        )
    for x in range(GRID_SIZE, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(
            surface=screen,
            color=COLOR_GRID,
            start_pos=(x, 0),
            end_pos=(x, SCREEN_HEIGHT),
            width=1
        )


snake = Snake(5)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    pressed_keys = pygame.key.get_pressed()
    snake.update(pressed_keys)

    draw_background(screen)
    for sprite in snake.body:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(10)


pygame.quit()
