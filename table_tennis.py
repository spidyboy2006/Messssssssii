"""
Simple Table Tennis (Pong) game in Python using pygame.

Controls:
    Player (left paddle): W / S  or  Up Arrow / Down Arrow
    Quit: close the window or press ESC

Install pygame first if you don't have it:
    pip install pygame
"""

import pygame
import random
import sys

pygame.init()

# ---------- Settings ----------
WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_SIZE = 12
PADDLE_SPEED = 6
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
WINNING_SCORE = 5
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)

# ---------- Setup ----------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Table Tennis")
clock = pygame.time.Clock()
font_score = pygame.font.SysFont("Arial", 36)
font_msg = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 18)

# Paddles
player = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai = pygame.Rect(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_dx = BALL_SPEED_X * random.choice((1, -1))
ball_dy = BALL_SPEED_Y * random.choice((1, -1))

player_score = 0
ai_score = 0
game_over = False


def reset_ball():
    global ball_dx, ball_dy
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_dx = BALL_SPEED_X * random.choice((1, -1))
    ball_dy = BALL_SPEED_Y * random.choice((1, -1))


def draw():
    screen.fill(BLACK)

    # Middle dashed line
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 1, y, 2, 10))

    # Paddles and ball
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, ai)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Scores
    p_text = font_score.render(str(player_score), True, WHITE)
    a_text = font_score.render(str(ai_score), True, WHITE)
    screen.blit(p_text, (WIDTH // 2 - 60, 20))
    screen.blit(a_text, (WIDTH // 2 + 40, 20))

    if game_over:
        winner = "You Win!" if player_score > ai_score else "AI Wins!"
        msg = font_msg.render(winner, True, GREEN)
        sub = font_small.render("Press R to restart or ESC to quit", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()


def update():
    global ball_dx, ball_dy, player_score, ai_score, game_over

    if game_over:
        return

    # Ball movement
    ball.x += ball_dx
    ball.y += ball_dy

    # Bounce off top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy = -ball_dy

    # Paddle collisions
    if ball.colliderect(player) and ball_dx < 0:
        ball_dx = -ball_dx
        ball.left = player.right
    if ball.colliderect(ai) and ball_dx > 0:
        ball_dx = -ball_dx
        ball.right = ai.left

    # Scoring
    if ball.left <= 0:
        ai_score += 1
        reset_ball()
    elif ball.right >= WIDTH:
        player_score += 1
        reset_ball()

    if player_score >= WINNING_SCORE or ai_score >= WINNING_SCORE:
        game_over = True

    # Simple AI: follow the ball with a bit of lag
    if ai.centery < ball.centery - 10:
        ai.y += PADDLE_SPEED - 1
    elif ai.centery > ball.centery + 10:
        ai.y -= PADDLE_SPEED - 1
    ai.y = max(0, min(HEIGHT - PADDLE_HEIGHT, ai.y))


def restart():
    global player_score, ai_score, game_over
    player.centery = HEIGHT // 2
    ai.centery = HEIGHT // 2
    player_score = 0
    ai_score = 0
    game_over = False
    reset_ball()


# ---------- Main loop ----------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and game_over:
                restart()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.y -= PADDLE_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.y += PADDLE_SPEED
        player.y = max(0, min(HEIGHT - PADDLE_HEIGHT, player.y))

    update()
    draw()
    clock.tick(FPS)

pygame.quit()
sys.exit()
