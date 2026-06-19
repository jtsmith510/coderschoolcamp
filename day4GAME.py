import pygame, sys
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player paddle
player_x = 20
player_y = HEIGHT // 2 - 50
PADDLE_W = 15
PADDLE_H = 100
PADDLE_SPEED = 6

# AI paddle
ai_x = WIDTH - 20 - PADDLE_W
ai_y = HEIGHT // 2 - 50
AI_SPEED = 4

# Ball
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5
ball_dy = 4
BALL_SIZE = 15

# Score
player_score = 0
ai_score = 0
font = pygame.font.SysFont("Arial", 48)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: player_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN]: player_y += PADDLE_SPEED
    player_y = max(0, min(player_y, HEIGHT - PADDLE_H))

    # Move ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce off top and bottom
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_dy = -ball_dy

    # AI follows ball
    if ai_y + PADDLE_H // 2 < ball_y:
        ai_y += AI_SPEED
    elif ai_y + PADDLE_H // 2 > ball_y:
        ai_y -= AI_SPEED
    ai_y = max(0, min(ai_y, HEIGHT - PADDLE_H))

    # Ball bounces off player paddle
    if (ball_x <= player_x + PADDLE_W and
        player_y < ball_y + BALL_SIZE and
        ball_y < player_y + PADDLE_H):
        ball_dx = abs(ball_dx)

    # Ball bounces off AI paddle
    if (ball_x + BALL_SIZE >= ai_x and
        ai_y < ball_y + BALL_SIZE and
        ball_y < ai_y + PADDLE_H):
        ball_dx = -abs(ball_dx)

    # Scoring
    if ball_x < 0:
        ai_score += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = 5
        ball_dy = 4

    if ball_x > WIDTH:
        player_score += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = -5
        ball_dy = 4

    # Draw
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    pygame.draw.rect(screen, WHITE, (player_x, player_y, PADDLE_W, PADDLE_H))
    pygame.draw.rect(screen, WHITE, (ai_x, ai_y, PADDLE_W, PADDLE_H))
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
    screen.blit(font.render(str(player_score), True, WHITE), (WIDTH // 4, 20))
    screen.blit(font.render(str(ai_score), True, WHITE), (3 * WIDTH // 4, 20))
    pygame.display.flip()
    clock.tick(60)
