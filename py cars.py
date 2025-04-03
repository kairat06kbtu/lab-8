import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Определение цветов
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

# Параметры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0  # Счетчик собранных монет

# Шрифты для отображения текста
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Создание окна игры
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# Загрузка и масштабирование фона
background = pygame.image.load("Road.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Функция для отрисовки фона
def draw_background():
    DISPLAYSURF.blit(background, (0, 0))

# Класс вражеской машины
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.image = pygame.transform.scale(self.image, (80, 120))  # Увеличен размер
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)  # Появление сверху

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = -50  # Возвращение наверх
            self.rect.center = (random.randint(30, 370), -50)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.image = pygame.transform.scale(self.image, (80, 120))  # Увеличен размер
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Класс монет
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)  # Появление сверху

    def move(self):
        global COINS
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = -50  # Возвращение наверх
            self.rect.center = (random.randint(30, 370), -50)

# Создание групп спрайтов
enemies = pygame.sprite.Group()
E1 = Enemy()
enemies.add(E1)

coins = pygame.sprite.Group()
C1 = Coin()
coins.add(C1)

all_sprites = pygame.sprite.Group()
P1 = Player()
all_sprites.add(P1, E1, C1)

# Увеличение скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Игровой цикл
while True:     
    for event in pygame.event.get():              
        if event.type == INC_SPEED:
            SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    draw_background()
    
    # Отображение счета и количества собранных монет
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_display = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coins_display, (SCREEN_WIDTH - 100, 10))
    
    # Движение и отрисовка всех спрайтов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    # Проверка столкновения игрока с врагами
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.mp3').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    # Проверка столкновения игрока с монетами
    if pygame.sprite.spritecollideany(P1, coins):
        COINS += 1
        for coin in coins:
            coin.rect.top = -50  # Возвращение монеты наверх
            coin.rect.center = (random.randint(30, 370), -50)
    
    pygame.display.update()
    FramePerSec.tick(FPS)
