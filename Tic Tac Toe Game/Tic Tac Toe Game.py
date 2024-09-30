import pygame
import sys

# Initialize Pygame
pygame.init()

# Colors
BACKGROUND = (240, 240, 245)  # Light grayish blue
GRID_COLOR = (180, 180, 200)  # Light purple
X_COLOR = (255, 100, 100)  # Light red
O_COLOR = (100, 100, 255)  # Light blue
TEXT_COLOR = (60, 60, 80)  # Dark blue-gray
BUTTON_COLOR = (120, 220, 180)  # Light green
BUTTON_HOVER_COLOR = (100, 200, 160)  # Slightly darker green

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tic Tac Toe")

# Game variables
board = [[''] * 3 for _ in range(3)]
current_player = 'X'
game_over = False
winner = None
player1_name = ''
player2_name = ''

def draw_board():
    cell_width = WIDTH // 3
    cell_height = HEIGHT // 3
    for i in range(1, 3):
        pygame.draw.line(screen, GRID_COLOR, (i * cell_width, 0), (i * cell_width, HEIGHT), 5)
        pygame.draw.line(screen, GRID_COLOR, (0, i * cell_height), (WIDTH, i * cell_height), 5)

def draw_symbols():
    cell_width = WIDTH // 3
    cell_height = HEIGHT // 3
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                x = col * cell_width + cell_width // 2
                y = row * cell_height + cell_height // 2
                pygame.draw.line(screen, X_COLOR, (x - 50, y - 50), (x + 50, y + 50), 10)
                pygame.draw.line(screen, X_COLOR, (x + 50, y - 50), (x - 50, y + 50), 10)
            elif board[row][col] == 'O':
                x = col * cell_width + cell_width // 2
                y = row * cell_height + cell_height // 2
                pygame.draw.circle(screen, O_COLOR, (x, y), 50, 10)

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def is_board_full():
    return all(all(cell != '' for cell in row) for row in board)

def reset_game():
    global board, current_player, game_over, winner
    board = [[''] * 3 for _ in range(3)]
    current_player = 'X'
    game_over = False
    winner = None

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def get_player_names():
    global player1_name, player2_name
    font = pygame.font.Font(None, 36)
    input_box1 = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 50)
    input_box2 = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
    color_inactive = GRID_COLOR
    color_active = X_COLOR
    color1 = color_inactive
    color2 = color_inactive
    active1 = False
    active2 = False
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = not active1
                else:
                    active1 = False
                if input_box2.collidepoint(event.pos):
                    active2 = not active2
                else:
                    active2 = False
                color1 = color_active if active1 else color_inactive
                color2 = color_active if active2 else color_inactive
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        active1 = False
                        active2 = True
                    elif event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    else:
                        player1_name += event.unicode
                    player1_name = player1_name[:15]
                elif active2:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    else:
                        player2_name += event.unicode
                    player2_name = player2_name[:15]

        screen.fill(BACKGROUND)
        draw_text("Player 1:", font, TEXT_COLOR, WIDTH // 2, HEIGHT // 3 - 20)
        draw_text("Player 2:", font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 20)
        
        txt_surface1 = font.render(player1_name, True, color1)
        txt_surface2 = font.render(player2_name, True, color2)
        width1 = max(WIDTH // 2, txt_surface1.get_width() + 10)
        width2 = max(WIDTH // 2, txt_surface2.get_width() + 10)
        input_box1.w = width1
        input_box2.w = width2
        screen.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 5))
        screen.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))
        pygame.draw.rect(screen, color1, input_box1, 2)
        pygame.draw.rect(screen, color2, input_box2, 2)

        pygame.display.flip()

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

def show_result_screen():
    screen.fill(BACKGROUND)
    font = pygame.font.Font(None, 72)
    if winner == 'Tie':
        draw_text("It's a tie!", font, TEXT_COLOR, WIDTH // 2, HEIGHT // 3)
    else:
        winner_name = player1_name if winner == 'X' else player2_name
        draw_text(f"{winner_name} wins!", font, TEXT_COLOR, WIDTH // 2, HEIGHT // 3)
    
    draw_button("Restart", WIDTH // 4, 2 * HEIGHT // 3, WIDTH // 4, 50, reset_game)
    draw_button("Quit", 2 * WIDTH // 4, 2 * HEIGHT // 3, WIDTH // 4, 50, sys.exit)

def main():
    global WIDTH, HEIGHT, screen, current_player, game_over, winner

    get_player_names()

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.size
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                col = x // (WIDTH // 3)
                row = y // (HEIGHT // 3)
                if board[row][col] == '':
                    board[row][col] = current_player
                    winner = check_winner()
                    if winner:
                        game_over = True
                    elif is_board_full():
                        game_over = True
                        winner = 'Tie'
                    current_player = 'O' if current_player == 'X' else 'X'

        if game_over:
            show_result_screen()
        else:
            screen.fill(BACKGROUND)
            draw_board()
            draw_symbols()

            current_name = player1_name if current_player == 'X' else player2_name
            draw_text(f"{current_name}'s turn ({current_player})", font, TEXT_COLOR, WIDTH // 2, 30)

            draw_text(f"{player1_name} (X)", font, X_COLOR, WIDTH // 4, HEIGHT - 30)
            draw_text(f"{player2_name} (O)", font, O_COLOR, 3 * WIDTH // 4, HEIGHT - 30)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()