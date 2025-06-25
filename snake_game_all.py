import pygame
import random
import sys

# Initialize
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont("comicsans", 30)
game_over_font = pygame.font.SysFont("comicsans", 50)

# Sounds (Optional: Add sound files to folder)
# pygame.mixer.init()
# eat_sound = pygame.mixer.Sound('eat.wav')
# game_over_sound = pygame.mixer.Sound('game_over.wav')

# Setup display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game by Rajaveer")


def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(win, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(win, GRAY, (0, y), (WIDTH, y))


def draw_snake(snake):
    for idx, block in enumerate(snake):
        color = GREEN if idx == 0 else DARK_GREEN
        pygame.draw.rect(win, color, (*block, BLOCK_SIZE, BLOCK_SIZE))


def draw_food(pos):
    pygame.draw.rect(win, RED, (*pos, BLOCK_SIZE, BLOCK_SIZE))


def get_random_food(snake):
    while True:
        x = random.randint(0, COLS - 1) * BLOCK_SIZE
        y = random.randint(0, ROWS - 1) * BLOCK_SIZE
        if (x, y) not in snake:
            return (x, y)


def show_message(msg, size, color, center):
    font_obj = pygame.font.SysFont("comicsans", size)
    text = font_obj.render(msg, True, color)
    text_rect = text.get_rect(center=center)
    win.blit(text, text_rect)


def start_screen():
    win.fill(WHITE)
    show_message("🐍 Snake Game", 50, BLACK, (WIDTH//2, HEIGHT//3))
    show_message("Press any key to start", 30, BLACK, (WIDTH//2, HEIGHT//2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False


def game_loop():
    clock = pygame.time.Clock()
    snake = [(WIDTH//2, HEIGHT//2)]
    direction = (BLOCK_SIZE, 0)  # Moving right
    food = get_random_food(snake)
    score = 0

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, BLOCK_SIZE):
                    direction = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -BLOCK_SIZE):
                    direction = (0, BLOCK_SIZE)
                elif event.key == pygame.K_LEFT and direction != (BLOCK_SIZE, 0):
                    direction = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-BLOCK_SIZE, 0):
                    direction = (BLOCK_SIZE, 0)

        # Move snake
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Check collision
        if (head in snake) or not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
            return score  # Game over

        snake.insert(0, head)

        # Eat food
        if head == food:
            # eat_sound.play()
            score += 1
            food = get_random_food(snake)
        else:
            snake.pop()

        # Drawing
        win.fill(WHITE)
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        show_message(f"Score: {score}", 25, BLACK, (60, 20))
        pygame.display.update()


def game_over_screen(score):
    win.fill(WHITE)
    show_message("💀 Game Over", 50, RED, (WIDTH//2, HEIGHT//3))
    show_message(f"Your Score: {score}", 30, BLACK, (WIDTH//2, HEIGHT//2))
    show_message("Press R to Restart or Q to Quit", 25, BLACK, (WIDTH//2, HEIGHT//1.5))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    start_screen()
    score = game_loop()
    # game_over_sound.play()
    game_over_screen(score)


if __name__ == "__main__":
    main()
