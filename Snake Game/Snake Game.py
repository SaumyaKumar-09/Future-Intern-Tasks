import pygame
import sys
import random
import json
import os

# Initialize Pygame
pygame.init()

# Colors
BACKGROUND = (240, 240, 245)  # Light grayish blue
SNAKE_COLOR = (100, 200, 100)  # Light green
FOOD_COLOR = (255, 100, 100)  # Light red
TEXT_COLOR = (60, 60, 80)  # Dark blue-gray
BUTTON_COLOR = (120, 220, 180)  # Light green
BUTTON_HOVER_COLOR = (100, 200, 160)  # Slightly darker green

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Snake Game")

# Game variables
GRID_SIZE = 20
snake = [(WIDTH // 2, HEIGHT // 2)]
snake_dir = (GRID_SIZE, 0)
food = None
score = 0
high_score = 0
high_score_name = ""
game_over = False
speed = 5  # Initial speed
food_eaten = 0  # Counter for eaten food
player_name = ""

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
high_score_file = os.path.join(script_dir, "snake_high_score.json")

def load_high_score():
    global high_score, high_score_name
    try:
        with open(high_score_file, "r") as file:
            data = json.load(file)
            high_score = data["score"]
            high_score_name = data["name"]
    except FileNotFoundError:
        high_score = 0
        high_score_name = ""

def save_high_score():
    with open(high_score_file, "w") as file:
        json.dump({"score": high_score, "name": high_score_name}, file)

def get_new_food():
    while True:
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        if (x, y) not in snake:
            return (x, y)

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (*segment, GRID_SIZE, GRID_SIZE))

def draw_food():
    if food:
        pygame.draw.rect(screen, FOOD_COLOR, (*food, GRID_SIZE, GRID_SIZE))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))
    
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)

def reset_game():
    global snake, snake_dir, food, score, game_over, speed, food_eaten
    snake = [(WIDTH // 2, HEIGHT // 2)]
    snake_dir = (GRID_SIZE, 0)
    food = get_new_food()
    score = 0
    game_over = False
    speed = 5  # Reset speed to initial value
    food_eaten = 0
    get_player_name()  # Ask for player name every time the game is restarted

def show_result_screen():
    screen.fill(BACKGROUND)
    font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 36)
    draw_text("Game Over!", font, TEXT_COLOR, WIDTH // 2, HEIGHT // 4)
    draw_text(f"Your Score: {score}", font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(f"High Score: {high_score} by {high_score_name}", small_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 50)
    
    draw_button("Restart", WIDTH // 4, 3 * HEIGHT // 4, WIDTH // 4, 50, reset_game)
    draw_button("Quit", 2 * WIDTH // 4, 3 * HEIGHT // 4, WIDTH // 4, 50, sys.exit)

def get_player_name():
    global player_name
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player_name = text
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                    text = text[:15]  # Limit name to 15 characters

        screen.fill(BACKGROUND)
        draw_text("Enter Your Name:", font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 40)
        
        txt_surface = font.render(text, True, color)
        width = max(WIDTH // 2, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

def main():
    global WIDTH, HEIGHT, screen, snake_dir, food, score, high_score, high_score_name, game_over, speed, food_eaten, player_name

    load_high_score()
    get_player_name()  # Ask for player name at the start of the game

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    food = get_new_food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score()
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                old_surface_saved = screen
                WIDTH, HEIGHT = event.size
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                screen.blit(old_surface_saved, (0, 0))
                del old_surface_saved
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP and snake_dir != (0, GRID_SIZE):
                    snake_dir = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -GRID_SIZE):
                    snake_dir = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and snake_dir != (GRID_SIZE, 0):
                    snake_dir = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-GRID_SIZE, 0):
                    snake_dir = (GRID_SIZE, 0)

        if not game_over:
            # Move snake
            new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

            # Check for collisions
            if (new_head in snake or 
                new_head[0] < 0 or new_head[0] >= WIDTH or 
                new_head[1] < 0 or new_head[1] >= HEIGHT):
                game_over = True
                if score > high_score:
                    high_score = score
                    high_score_name = player_name
                    save_high_score()
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food_eaten += 1
                    food = get_new_food()
                    if food_eaten % 5 == 0:
                        speed += 1  # Increase speed every 5 food items
                else:
                    snake.pop()

            # Draw game
            screen.fill(BACKGROUND)
            draw_snake()
            draw_food()
            draw_text(f"Score: {score}", font, TEXT_COLOR, WIDTH // 2, 30)

        else:
            show_result_screen()

        pygame.display.flip()
        clock.tick(speed)  # Use variable speed

if __name__ == "__main__":
    main()