import pygame, sys, random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Meteors!")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 52, bold=True)

# Colors
BG = (10, 10, 30)
HERO_C = (80, 200, 120)
ROCK_C = (160, 100, 60)
WHITE = (255, 255, 255)
RED = (220, 60, 60)
YELLOW = (255, 220, 50)


def reset_game():
    global player, meteors, lives, score, spawn_timer, meteor_speed
    player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 50)
    meteors = []
    lives = 3
    score = 0
    spawn_timer = 0
    meteor_speed = 4


STATE = "START"  # "START", "PLAYING", "GAMEOVER"
reset_game()

while True:
    dt = clock.tick(60)

    # ── EVENTS ────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if STATE == "START" and event.key == pygame.K_SPACE:
                STATE = "PLAYING"
            if STATE == "GAMEOVER" and event.key == pygame.K_r:
                reset_game()
                STATE = "PLAYING"

    # ── UPDATE (only when playing) ─────────────────
    if STATE == "PLAYING":
        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 6
        if keys[pygame.K_RIGHT]:
            player.x += 6
        player.x = max(0, min(player.x, WIDTH - player.width))

        # Spawn new meteors
        spawn_timer += 1
        if spawn_timer >= 40:
            spawn_timer = 0
            mx = random.randint(0, WIDTH - 40)
            meteors.append(pygame.Rect(mx, -40, 40, 40))

        # Move meteors down
        for m in meteors[:]:
            m.y += meteor_speed
            if m.y > HEIGHT:
                meteors.remove(m)
                score += 10  # survived a meteor!
            elif m.colliderect(player):
                meteors.remove(m)
                lives -= 1

        # Speed up over time
        meteor_speed = 4 + score // 100

        if lives <= 0:
            STATE = "GAMEOVER"

    # ── DRAW ──────────────────────────────────────
    screen.fill(BG)

    if STATE == "START":
        t = big_font.render("☄️ DODGE THE METEORS", True, WHITE)
        s = font.render("Press SPACE to start", True, YELLOW)
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 200))
        screen.blit(s, (WIDTH // 2 - s.get_width() // 2, 310))

    elif STATE == "PLAYING":
        pygame.draw.rect(screen, HERO_C, player)
        for m in meteors:
            pygame.draw.ellipse(screen, ROCK_C, m)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Lives: {'❤️' * lives}", True, RED), (600, 10))

    elif STATE == "GAMEOVER":
        g = big_font.render("GAME OVER", True, RED)
        sc = font.render(f"Final Score: {score} | Press R to restart", True, WHITE)
        screen.blit(g, (WIDTH // 2 - g.get_width() // 2, 200))
        screen.blit(sc, (WIDTH // 2 - sc.get_width() // 2, 300))

    pygame.display.flip()
