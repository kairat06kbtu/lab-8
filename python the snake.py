import pygame, random, sys


pygame.init()


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
GRID_SIZE = 20 


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")


class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]  
        self.direction = "RIGHT"
        self.growing = False

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == "LEFT":
            new_head = (head_x - GRID_SIZE, head_y)
        else:
            new_head = (head_x + GRID_SIZE, head_y)
        
        self.body.insert(0, new_head)
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def grow(self):
        self.growing = True

    def check_collision(self):
        head_x, head_y = self.body[0]
        
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            return True
       
        if (head_x, head_y) in self.body[1:]:
            return True
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, GRID_SIZE, GRID_SIZE))


class Food:
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)

    def random_position(self, snake_body):
        while True:
            x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
            y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
            if (x, y) not in snake_body:
                return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self.position, GRID_SIZE, GRID_SIZE))


snake = Snake()
food = Food(snake.body)
speed = 10
score = 0
level = 1

clock = pygame.time.Clock()


running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != "DOWN":
                snake.direction = "UP"
            elif event.key == pygame.K_DOWN and snake.direction != "UP":
                snake.direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                snake.direction = "RIGHT"
    
    
    snake.move()
    
    
    if snake.check_collision():
        running = False
    
    
    if snake.body[0] == food.position:
        snake.grow()
        food = Food(snake.body)
        score += 1
    
    
    if score % 3 == 0 and score != 0:
        level = score // 3 + 1
        speed = 10 + (level - 1) * 2
    
    
    snake.draw(screen)
    food.draw(screen)
    
    
    font = pygame.font.SysFont("Verdana", 20)
    score_text = font.render(f"Очки: {score}", True, BLACK)
    level_text = font.render(f"Уровень: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
sys.exit()