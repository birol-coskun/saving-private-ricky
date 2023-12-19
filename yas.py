import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Saving Private Ricky")

# Spaceship image
player_image = pygame.image.load("data/player1.gif")
player_image = pygame.transform.scale(player_image, (50, 50))

# Spaceship starting position and speed
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - player_size
player_speed = 5

# Enemy genes
gene_size = 50
gene_speed = 3
genes = []

# Bullet
bullet_size = 10
bullet_speed = 5
bullets = []

# Score and time
score = 0
font = pygame.font.Font(None, 36)
start_time = pygame.time.get_ticks()

# Game state
game_over = False
restart_prompt = False  # Control flag for restart prompt

# Game difficulty
initial_enemy_count = 10
enemy_spawn_time = 3
last_spawn_time = pygame.time.get_ticks()

# Shooting control
can_shoot = True
shoot_cooldown = 500
last_shoot_time = pygame.time.get_ticks()

# Load alien image
alien_image = pygame.image.load("data/alien1.gif")
alien_image = pygame.transform.scale(alien_image, (gene_size, gene_size))

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and can_shoot:
            # Shooting control and bullet creation
            bullet_x = player_x + player_size // 2 - bullet_size // 2
            bullet_y = player_y
            bullets.append([bullet_x, bullet_y])
            can_shoot = False
            last_shoot_time = pygame.time.get_ticks()

    if not game_over:
        # Spaceship movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_size:
            player_x += player_speed

        # Enemy gene creation
        current_time = pygame.time.get_ticks()
        if current_time - start_time < 1000 * initial_enemy_count:
            # Add enemies at the beginning
            if current_time - last_spawn_time > enemy_spawn_time * 1000:
                gene_x = random.randint(0, width - gene_size)
                gene_y = 0
                genes.append([gene_x, gene_y])
                last_spawn_time = current_time
        else:
            # Add enemies every 3 seconds after the beginning
            if current_time - last_spawn_time > enemy_spawn_time * 1000:
                for _ in range(score // 5 + 1):
                    gene_x = random.randint(0, width - gene_size)
                    gene_y = 0
                    genes.append([gene_x, gene_y])
                last_spawn_time = current_time

        # Enemy gene movement and score update
        for gene in genes:
            gene[1] += gene_speed
            if gene[1] > height:
                genes.remove(gene)
                game_over = True  # End the game when an alien reaches the bottom
                restart_prompt = True  # Show restart prompt

        # Bullet movement and collision control
        for bullet in bullets:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
                can_shoot = True

            # Alien collision control
            for gene in genes:
                gene_rect = pygame.Rect(gene[0], gene[1], gene_size, gene_size)
                bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)

                if gene_rect.colliderect(bullet_rect):
                    genes.remove(gene)
                    bullets.remove(bullet)
                    score += 1
                    can_shoot = True

        # Calculate elapsed time
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        # Check and update difficulty level
        gene_speed = 3 + elapsed_time // 20  # Increase speed every 20 seconds

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the spaceship
        screen.blit(player_image, (player_x, player_y))

        # Draw enemy genes
        for gene in genes:
            screen.blit(alien_image, (gene[0], gene[1]))

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 255), [bullet[0], bullet[1], bullet_size, bullet_size])

        # Draw the score and time on the screen
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        time_text = font.render(f"Time: {elapsed_time} seconds", True, (255, 255, 255))
        screen.blit(time_text, (10, 40))

    else:
        # Draw the game over message
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (width // 2 - 100, height // 2 - 20))

        if restart_prompt:
            # Draw the restart prompt
            restart_text = font.render("Do you want to play again? (Y/N)", True, (255, 255, 255))
            screen.blit(restart_text, (width // 2 - 160, height // 2 + 20))

            # Check the user's response
            keys = pygame.key.get_pressed()
            if keys[pygame.K_y]:
                # If yes, reset the game
                game_over = False
                genes = []
                bullets = []
                score = 0
                start_time = pygame.time.get_ticks()
                restart_prompt = False
            elif keys[pygame.K_n]:
                # If no, close the game
                pygame.quit()
                sys.exit()

    # Shooting cooldown control
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - last_shoot_time >= shoot_cooldown:
            can_shoot = True

    # Update the screen
    pygame.display.flip()

    # FPS limit
    clock.tick(60)
