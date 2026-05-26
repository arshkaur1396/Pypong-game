import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the screen
WIDTH, HEIGHT = 1530, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Custom Pong Game")
pygame.display.update()

# Game variables
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = random.choice([-5, 5])
ball_dy = random.choice([-5, 5])
paddle_width = 30
paddle_height = 150
player_y = HEIGHT // 2 - paddle_height // 2
computer_y = HEIGHT // 2 - paddle_height // 2
player_score = 0
computer_score = 0
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
is_game_started = False
is_paused = False
current_level = 'Easy'  # Initialize current level

# Load sound effects
bounce_sound = pygame.mixer.Sound("plastic-ball-bounce-14790.mp3")
score_sound = pygame.mixer.Sound("short-success-sound-glockenspiel-treasure-video-game-6346.mp3")

# Define levels with parameters
levels = {
    'Easy': {'ball_speed': 0.9, 'paddle_speed': 5, 'ai_reaction': 2},
    'Medium': {'ball_speed': 1.6, 'paddle_speed': 7, 'ai_reaction': 4},
    'Hard': {'ball_speed': 3, 'paddle_speed': 10, 'ai_reaction': 6}
}

# Initialize a variable to track dropdown state
dropdown_open = False


# Function to handle level selection
def select_level(level):
    global current_level
    current_level = level


# Function to draw drop-down list
def draw_dropdown():
    global dropdown_open

    dropdown_rect = pygame.Rect(WIDTH // 2 - 75, 20, 150, 50)
    pygame.draw.rect(screen, WHITE, dropdown_rect)
    pygame.draw.line(screen, BLACK, (WIDTH // 2 - 75, 20), (WIDTH // 2 + 75, 20), 2)
    pygame.draw.line(screen, BLACK, (WIDTH // 2 - 75, 70), (WIDTH // 2 + 75, 70), 2)
    dropdown_text = font.render(current_level, True, BLACK)
    screen.blit(dropdown_text, (WIDTH // 2 - dropdown_text.get_width() // 2, 35))

    # Check if mouse is hovering over dropdown or its options
    mouse_pos = pygame.mouse.get_pos()
    if dropdown_rect.collidepoint(mouse_pos):
        dropdown_open = True
    elif not any(level_rect.collidepoint(mouse_pos) for level_rect in level_rects):
        dropdown_open = False

    # Draw dropdown options
    if dropdown_open:
        for i, (level, level_rect) in enumerate(zip(levels.keys(), level_rects)):
            pygame.draw.rect(screen, WHITE, level_rect)
            level_text = font.render(level, True, BLACK)
            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 35 + (i + 1) * 50))

            # Check for click on level option
            if level_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:  # Left mouse button
                select_level(level)


# Function to draw paddles
def draw_paddle(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, paddle_width, paddle_height))


# Function to draw ball
def draw_ball(x, y):
    pygame.draw.circle(screen, RED, (x, y), ball_radius)


# Function to display scores
def display_scores():
    player_text = font.render(f"Player1: {player_score}", True, WHITE)
    computer_text = font.render(f"Player2(Computer): {computer_score}", True, WHITE)
    screen.blit(player_text, (50, 50))
    screen.blit(computer_text, (WIDTH - 300, 50))


# Function to display winner
def display_winner(winner):
    winner_text = font.render(f"Winner: Player{winner}", True, WHITE)
    screen.blit(winner_text, (WIDTH // 2 - 100, HEIGHT // 5))


# Function to handle button clicks
def handle_button_click(mouse_pos, button_rect, action):
    if button_rect.collidepoint(mouse_pos):
        action()


# Function to start the game
def start_game():
    global is_game_started
    is_game_started = True


# Function to pause/resume the game
def pause_resume_game():
    global is_paused
    is_paused = not is_paused


# Function to quit the game
def quit_game():
    pygame.quit()
    sys.exit()


# Main game loop
running = True
while running:
    screen.fill(BLUE)

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_game()
            elif event.key == pygame.K_ESCAPE:
                quit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                handle_button_click(mouse_pos, start_button_rect, start_game)
                handle_button_click(mouse_pos, pause_resume_button_rect, pause_resume_game)
                handle_button_click(mouse_pos, quit_button_rect, quit_game)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= levels[current_level]['paddle_speed']
    if keys[pygame.K_DOWN] and player_y < HEIGHT - paddle_height:
        player_y += levels[current_level]['paddle_speed']

    if is_game_started and not is_paused:
        ball_x += levels[current_level]['ball_speed'] * ball_dx
        ball_y += levels[current_level]['ball_speed'] * ball_dy

        # Computer AI speed based on level
        if computer_y < ball_y:
            computer_y += levels[current_level]['ai_reaction']
        elif computer_y > ball_y:
            computer_y -= levels[current_level]['ai_reaction']

        # Ball collision with walls
        if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
            ball_dy = -ball_dy
            bounce_sound.play()

        # Ball collision with paddles
        if ball_x - ball_radius <= paddle_width and player_y < ball_y < player_y + paddle_height:
           ball_dx = -ball_dx
           bounce_sound.play()
        elif ball_x + ball_radius >= WIDTH - paddle_width and computer_y < ball_y < computer_y + paddle_height:
            ball_dx = -ball_dx
            bounce_sound.play()

         # Scoring
        if ball_x - ball_radius <= 0:
            computer_score += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = random.choice([-5, 5])
            ball_dy = random.choice([-5, 5])
            is_game_started = False
            score_sound.play()
        elif ball_x + ball_radius >= WIDTH:
             player_score += 1
             ball_x, ball_y = WIDTH // 2, HEIGHT // 2
             ball_dx = random.choice([-5, 5])
             ball_dy = random.choice([-5, 5])
             is_game_started = False
             score_sound.play()

     #draw paddles
    draw_paddle(0, player_y)
    draw_paddle(WIDTH - paddle_width, computer_y)
    draw_ball(ball_x, ball_y)
    display_scores()

    if player_score >= 10:
       display_winner(1)
    elif computer_score >= 10:
       display_winner(2)

   # Store level rects for dropdown interaction
    level_rects = [pygame.Rect(WIDTH // 2 - 75, 20 + (i + 1) * 50, 150, 50) for i in range(len(levels))]

   # Draw dropdown list
    draw_dropdown()

   # Draw buttons
    start_button_rect = pygame.draw.rect(screen, WHITE, (50, HEIGHT - 80, 100, 50))
    pause_resume_button_rect = pygame.draw.rect(screen, WHITE, (200, HEIGHT - 80, 180, 50))
    quit_button_rect = pygame.draw.rect(screen, WHITE, (400, HEIGHT - 80, 100, 50))

    start_button_text = font.render("Start", True, BLACK)
    screen.blit(start_button_text, (75, HEIGHT - 65))
    pause_resume_button_text = font.render("Pause/Resume", True, BLACK)
    screen.blit(pause_resume_button_text, (205, HEIGHT - 65))
    quit_button_text = font.render("Quit", True, BLACK)
    screen.blit(quit_button_text, (435, HEIGHT - 65))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
