import pygame
import sys
import random

# Pygame'ı başlat
pygame.init()

# Ekran ayarları
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("CALL Game")

# Uzay gemisi resmi
player_image = pygame.image.load("data/player1.gif")
player_image = pygame.transform.scale(player_image, (50, 50))

# Uzay gemisi başlangıç konumu ve hızı
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - player_size
player_speed = 5

# Düşman genleri
gene_size = 50
gene_speed = 3
genes = []

# Mermi
bullet_size = 10
bullet_speed = 5
bullets = []

# Skor ve süre
score = 0
font = pygame.font.Font(None, 36)
start_time = pygame.time.get_ticks()

# Oyun durumu
game_over = False
restart_prompt = False  # Yeniden başlatma sorusu için kontrol flag'i

# Oyun zorluğu
difficulty_increase_time = 120
initial_gene_speed = 3

# Ateş etme kontrolü
can_shoot = True
shoot_cooldown = 500
last_shoot_time = pygame.time.get_ticks()

# Alien resmini yükle
alien_image = pygame.image.load("data/alien1.gif")
alien_image = pygame.transform.scale(alien_image, (gene_size, gene_size))

# Oyun döngüsü
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and can_shoot:
            # Ateş etme kontrolü ve mermi oluşturma
            bullet_x = player_x + player_size // 2 - bullet_size // 2
            bullet_y = player_y
            bullets.append([bullet_x, bullet_y])
            can_shoot = False
            last_shoot_time = pygame.time.get_ticks()

    if not game_over:
        # Uzay gemisi hareketi
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_size:
            player_x += player_speed

        # Düşman geni oluşturma
        if random.randint(1, 100) < 5:  # Her frame'de 5% şansla
            gene_x = random.randint(0, width - gene_size)
            gene_y = 0
            genes.append([gene_x, gene_y])

        # Düşman geni hareketi ve skor güncelleme
        for gene in genes:
            gene[1] += gene_speed
            if gene[1] > height:
                genes.remove(gene)
                game_over = True  # Alien alt kenarına ulaştığında oyunu bitir
                restart_prompt = True  # Yeniden başlatma sorusunu göster

        # Mermi hareketi ve çarpışma kontrolü
        for bullet in bullets:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
                can_shoot = True

            # Alien çarpışma kontrolü
            for gene in genes:
                gene_rect = pygame.Rect(gene[0], gene[1], gene_size, gene_size)
                bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)

                if gene_rect.colliderect(bullet_rect):
                    genes.remove(gene)
                    bullets.remove(bullet)
                    score += 1
                    can_shoot = True

        # Geçen süreyi hesapla
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        # Zorluk seviyesini kontrol et ve güncelle
        if elapsed_time > difficulty_increase_time:
            gene_speed = initial_gene_speed + elapsed_time - difficulty_increase_time

        # Ekran temizleme
        screen.fill((0, 0, 0))

        # Uzay gemisini çizme
        screen.blit(player_image, (player_x, player_y))

        # Düşman genlerini çizme
        for gene in genes:
            screen.blit(alien_image, (gene[0], gene[1]))

        # Mermileri çizme
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 255), [bullet[0], bullet[1], bullet_size, bullet_size])

        # Skoru ve süreyi ekrana yazdırma
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        time_text = font.render(f"Time: {elapsed_time} seconds", True, (255, 255, 255))
        screen.blit(time_text, (10, 40))

    else:
        # Oyun bitti mesajını ekrana yazdırma
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (width // 2 - 100, height // 2 - 20))

        if restart_prompt:
            # Yeniden oynamak ister misin? sorusu
            restart_text = font.render("Do you want to play again? (Y/N)", True, (255, 255, 255))
            screen.blit(restart_text, (width // 2 - 160, height // 2 + 20))

            # Kullanıcının cevabını kontrol et
            keys = pygame.key.get_pressed()
            if keys[pygame.K_y]:
                # Evet ise oyunu sıfırla
                game_over = False
                genes = []
                bullets = []
                score = 0
                start_time = pygame.time.get_ticks()
                restart_prompt = False
            elif keys[pygame.K_n]:
                # Hayır ise oyunu kapat
                pygame.quit()
                sys.exit()

    # Ateş etme cooldown kontrolü
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - last_shoot_time >= shoot_cooldown:
            can_shoot = True

    # Ekran güncelleme
    pygame.display.flip()

    # FPS sınırlama
    clock.tick(60)
