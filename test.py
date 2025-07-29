import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# Jugador
player = pygame.Rect(100, 300, 50, 50)
gravity = 0

# Balas
bullets = []

# Enemigos
enemies = [pygame.Rect(700, 300, 40, 40)]

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Disparo
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # disparar con F
                bullet = pygame.Rect(player.right, player.centery - 5, 10, 10)
                bullets.append(bullet)

    # Movimiento jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and player.bottom >= 300:
        gravity = -20
    gravity += 1
    player.y += gravity
    if player.bottom >= 300:
        player.bottom = 300

    # Mover balas
    for bullet in bullets:
        bullet.x += 10  # velocidad
    bullets = [b for b in bullets if b.x < 800]  # eliminar fuera de pantalla

    # Dibujar jugador
    pygame.draw.rect(screen, BLUE, player)

    # Dibujar y mover enemigos
    for enemy in enemies:
        enemy.x -= 2
        pygame.draw.rect(screen, RED, enemy)

    # Colisión bala-enemigo
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                if enemy in enemies:
                    enemies.remove(enemy)
                if bullet in bullets:
                    bullets.remove(bullet)
                break  # salir del loop interno

    # Dibujar balas
    for bullet in bullets:
        pygame.draw.rect(screen, (0, 0, 0), bullet)

    pygame.display.update()
    clock.tick(60)
