import pygame
import random
from pygame.constants import (
    KEYDOWN, K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, QUIT, K_UP, RLEACCEL
)
from pygame.time import Clock
from pygame.sprite import Sprite


pygame.init()

# custom event, generate a new enemy
ADDENEMY = pygame.USEREVENT + 1
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMY, 1000)
pygame.time.set_timer(ADDCLOUD, 1000)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('jet2.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right < SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('missile.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(
            random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
            random.randint(0, SCREEN_HEIGHT)
        ))
        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.left < -50:
            self.kill()


class Cloud(Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('cloud.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(
            random.randint(SCREEN_WIDTH+1, SCREEN_WIDTH+10),
            random.randint(0, SCREEN_HEIGHT)
        ))
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.left < -50:
            self.kill()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()

# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load('Apoxode_-_Electric_1.mp3')
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound('Rising_putter.ogg')
move_down_sound = pygame.mixer.Sound('Falling_putter.ogg')
collision_sound = pygame.mixer.Sound('Collision.ogg')

clock = Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == ADDENEMY:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        elif event.type == ADDCLOUD:
            cloud = Cloud()
            all_sprites.add(cloud)
            clouds.add(cloud)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()

    screen.fill((135, 206, 250))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
