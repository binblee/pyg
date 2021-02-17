import pygame
import random
from pygame.constants import (
    KEYDOWN,
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP, K_g,
    QUIT,
    RLEACCEL)
from pygame.sprite import Sprite

pygame.init()

GRID_SIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

POS_X_RANGE = SCREEN_WIDTH/GRID_SIZE
POS_Y_RANGE = SCREEN_HEIGHT/GRID_SIZE

NORTH = (0, -1 * GRID_SIZE)
SOUTH = (0, 1 * GRID_SIZE)
WEST = (-1 * GRID_SIZE, 0)
EAST = (1 * GRID_SIZE, 0)

INITIAL_SNAKE_LENGTH = 3
SNAKE_LENGTH_INC = 1


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
        self.last_tail_pos = self.body[-1].rect.topleft

    def update(self, pressed_keys):
        if pressed_keys[K_UP] and self.direction != SOUTH:
            self.direction = NORTH
        if pressed_keys[K_DOWN] and self.direction != NORTH:
            self.direction = SOUTH
        if pressed_keys[K_LEFT] and self.direction != EAST:
            self.direction = WEST
        if pressed_keys[K_RIGHT] and self.direction != WEST:
            self.direction = EAST
        self.last_tail_pos = self.body[-1].rect.topleft
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

    def inc_length(self):
        new_tail = SnakeBody(0)
        self.body.append(new_tail)
        new_tail.rect.topleft = self.last_tail_pos

    def get_positions(self):
        positions = []
        for bd in self.body:
            positions.append(bd.rect.topleft)
        return positions


class Food(Sprite):
    def __init__(self, avoid_positions):
        super().__init__()
        # self.surf = pygame.Surface((GRID_SIZE, GRID_SIZE))
        # self.surf.fill((200, 0, 0))
        self.surf = pygame.image.load('apple-32x32.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        pos = ()
        good_position = False
        while not good_position:
            pos = (random.randint(0, POS_X_RANGE-1) * GRID_SIZE,
                   random.randint(0, POS_Y_RANGE-1) * GRID_SIZE)
            if pos not in avoid_positions:
                good_position = True

        self.rect = self.surf.get_rect(topleft=pos)


def draw_background(screen, grid_on):
    COLOR_BACKGROUND = (0, 0, 0)
    COLOR_GRID = (200, 200, 200)
    screen.fill(COLOR_BACKGROUND)
    if grid_on:
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


# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load('Apoxode_-_Electric_1.mp3')
pygame.mixer.music.play(loops=-1)

# Sound sources: Jon Fincher
collision_sound = pygame.mixer.Sound('Collision.ogg')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

snake = Snake(INITIAL_SNAKE_LENGTH)
avoid_positions = snake.get_positions()
food = Food(avoid_positions)
running = True
clock = pygame.time.Clock()
grid_on = False
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    pressed_keys = pygame.key.get_pressed()
    snake.update(pressed_keys)
    if pygame.sprite.collide_rect(food, snake.body[0]):
        snake.inc_length()
        food.kill()
        avoid_positions = snake.get_positions()
        food = Food(avoid_positions)
        collision_sound.play()
    if pressed_keys[K_g]:
        grid_on = not grid_on

    draw_background(screen, grid_on)
    for sprite in snake.body:
        screen.blit(sprite.surf, sprite.rect)
    screen.blit(food.surf, food.rect)

    pygame.display.flip()
    clock.tick(8)


pygame.quit()
