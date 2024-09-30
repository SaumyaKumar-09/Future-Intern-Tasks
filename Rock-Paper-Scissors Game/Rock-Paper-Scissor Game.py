import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = int(infoObject.current_w * 0.8), int(infoObject.current_h * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Rock Paper Scissors")

# Colors (unchanged)
BACKGROUND = (240, 248, 255)  # AliceBlue
TEXT = (70, 130, 180)  # SteelBlue
BUTTON = (135, 206, 250)  # LightSkyBlue
BUTTON_HOVER = (100, 149, 237)  # CornflowerBlue
ROCK_COLOR = (255, 160, 122)  # LightSalmon
PAPER_COLOR = (152, 251, 152)  # PaleGreen
SCISSORS_COLOR = (255, 182, 193)  # LightPink

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)
symbol_font = pygame.font.Font(None, 24)

# Game variables
choices = ["Rock", "Paper", "Scissors"]
player_score = 0
computer_score = 0

# Particle system (unchanged)
particles = []

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(5, 10)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.lifetime = random.randint(30, 60)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

def create_particles(x, y, color, count=20):
    for _ in range(count):
        particles.append(Particle(x, y, color))

def update_particles():
    for particle in particles[:]:
        particle.update()
        if particle.lifetime <= 0:
            particles.remove(particle)

def draw_particles(surface):
    for particle in particles:
        particle.draw(surface)

def draw_text(surface, text, pos, color=TEXT, font=font):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, text_rect)

def get_computer_choice():
    return random.choice(choices)

def determine_winner(player_choice, computer_choice):
    global player_score, computer_score
    if player_choice == computer_choice:
        return "It's a tie!"
    elif (
        (player_choice == "Rock" and computer_choice == "Scissors") or
        (player_choice == "Paper" and computer_choice == "Rock") or
        (player_choice == "Scissors" and computer_choice == "Paper")
    ):
        player_score += 1
        return "You win!"
    else:
        computer_score += 1
        return "Computer wins!"

def draw_hand(surface, choice, pos, scale=1.0):
    if choice == "Rock":
        pygame.draw.circle(surface, ROCK_COLOR, pos, int(30 * scale))
    elif choice == "Paper":
        pygame.draw.rect(surface, PAPER_COLOR, (pos[0] - int(25 * scale), pos[1] - int(35 * scale), int(50 * scale), int(70 * scale)))
    elif choice == "Scissors":
        pygame.draw.line(surface, SCISSORS_COLOR, (pos[0] - int(20 * scale), pos[1] - int(20 * scale)), (pos[0] + int(20 * scale), pos[1] + int(20 * scale)), int(10 * scale))
        pygame.draw.line(surface, SCISSORS_COLOR, (pos[0] - int(20 * scale), pos[1] + int(20 * scale)), (pos[0] + int(20 * scale), pos[1] - int(20 * scale)), int(10 * scale))

def main():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen
    clock = pygame.time.Clock()
    player_choice = None
    computer_choice = None
    result = ""

    # Smaller buttons with symbols
    quit_button = pygame.Rect(SCREEN_WIDTH - 40, 10, 30, 30)
    minimize_button = pygame.Rect(SCREEN_WIDTH - 80, 10, 30, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                quit_button.topleft = (SCREEN_WIDTH - 40, 10)
                minimize_button.topleft = (SCREEN_WIDTH - 80, 10)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if quit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
                elif minimize_button.collidepoint(mouse_x, mouse_y):
                    pygame.display.iconify()
                elif SCREEN_HEIGHT // 2 + 50 < mouse_y < SCREEN_HEIGHT // 2 + 90:
                    if SCREEN_WIDTH // 4 - 50 < mouse_x < SCREEN_WIDTH // 4 + 50:
                        player_choice = "Rock"
                    elif SCREEN_WIDTH // 2 - 50 < mouse_x < SCREEN_WIDTH // 2 + 50:
                        player_choice = "Paper"
                    elif 3 * SCREEN_WIDTH // 4 - 50 < mouse_x < 3 * SCREEN_WIDTH // 4 + 50:
                        player_choice = "Scissors"

                    if player_choice:
                        computer_choice = get_computer_choice()
                        result = determine_winner(player_choice, computer_choice)
                        create_particles(mouse_x, mouse_y, BUTTON_HOVER)

        screen.fill(BACKGROUND)

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for i, choice in enumerate(choices):
            button_rect = pygame.Rect(SCREEN_WIDTH // 4 * (i + 1) - 50, SCREEN_HEIGHT // 2 + 50, 100, 40)
            color = BUTTON_HOVER if button_rect.collidepoint(mouse_pos) else BUTTON
            pygame.draw.rect(screen, color, button_rect)
            draw_text(screen, choice, (SCREEN_WIDTH // 4 * (i + 1), SCREEN_HEIGHT // 2 + 70))

        # Draw quit and minimize buttons with symbols
        pygame.draw.rect(screen, BUTTON_HOVER if quit_button.collidepoint(mouse_pos) else BUTTON, quit_button)
        pygame.draw.rect(screen, BUTTON_HOVER if minimize_button.collidepoint(mouse_pos) else BUTTON, minimize_button)
        draw_text(screen, "×", quit_button.center, font=symbol_font)
        draw_text(screen, "_", minimize_button.center, font=symbol_font)

        # Draw scores
        draw_text(screen, f"Player: {player_score}", (SCREEN_WIDTH // 4, 50), font=large_font)
        draw_text(screen, f"Computer: {computer_score}", (3 * SCREEN_WIDTH // 4, 50), font=large_font)

        # Draw choices and result
        if player_choice and computer_choice:
            draw_text(screen, "You chose:", (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 - 30))
            draw_hand(screen, player_choice, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + 70), scale=1.5)  # Moved 50px down
            draw_text(screen, "Computer chose:", (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 - 30))
            draw_hand(screen, computer_choice, (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + 70), scale=1.5)  # Moved 50px down
            draw_text(screen, result, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 170), font=large_font)  # Adjusted result position

        # Update and draw particles
        update_particles()
        draw_particles(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()