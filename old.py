import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()


snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

direction = 'RIGHT'
change_to = direction
food_pos = [random.randrange(1, (WIDTH//10)) * 10,
            random.randrange(1, (HEIGHT//10)) * 10]
food_spawn = True

score = 0

while True:
    # --- SECTION A: Only check for key presses here ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # --- SECTION B: Everything below must be OUTSIDE the event loop! ---
    # This makes the snake move even when you aren't touching the keys.

    # Fix direction change logic
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the head by 10 pixels
    if direction == 'UP':
        snake_pos[1] -= 10
    elif direction == 'DOWN':
        snake_pos[1] += 10
    elif direction == 'LEFT':
        snake_pos[0] -= 10
    elif direction == 'RIGHT':
        snake_pos[0] += 10

    # Update body
    snake_body.insert(0, list(snake_pos))

    # Check for food
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

        # Respawn food logic
        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH // 10)) * 10,
                        random.randrange(1, (HEIGHT // 10)) * 10]
            food_spawn = True

            # --- EVERYTHING BELOW MOVES TO THE LEFT (OUTSIDE+ if not food_spawn) ---
        screen.fill((0, 0, 0))

        # Draw Snake
        for block in snake_body:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(block[0], block[1], 10, 10))

        # Draw Food
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Draw Score
        font = pygame.font.SysFont('arial', 20)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Wall Collision
        if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10 or snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
            pygame.quit()
            sys.exit()

        # Self Collision
        for block in snake_body[1:]:
            if snake_pos == block:
                pygame.quit()
                sys.exit()

        # Final Update
        pygame.display.update()
        clock.tick(15)