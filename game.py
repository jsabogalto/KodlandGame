import pygame
from sys import exit

#inicio y configuracion de pantalla principal
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Juego de Jonathan")
clock = pygame.time.Clock()
#texto 
test_font = pygame.font.Font("public/Pixeltype.ttf", 50)
#configuracion del mapa
sky_surface = pygame.image.load("public/Sky.png").convert()
ground_surface = pygame.image.load("public/ground.png").convert()
#jugador
player_surface = pygame.image.load("public/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))
#primer enemigo
snail_surface = pygame.image.load("public/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))
#score
score_surface = test_font.render("Juego", False, "Green")
score_rect = score_surface.get_rect(center = (400, 50))
#gravity for player
gravity_player = 0

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
        if event.type == pygame.MOUSEMOTION:
            print(event.pos)
        
        if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
            if event.key == pygame.K_SPACE:
                gravity_player = -20


    #dibujar por pantalla
    #actualizar los obj1etos
    screen.blit(ground_surface, (0, 300))
    screen.blit(sky_surface, (0, 0))
    screen.blit(score_surface, score_rect)

    snail_rect.x -= 4
    if snail_rect.right <= 0 : snail_rect.left = 800

    

    # if player_rect.colliderect(snail_rect):
    #     print("collision")
    # else:
    #     print("Nothing")
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())
    # else:
    #     print("NOTHING")

    #collisions
    if snail_rect.colliderect(player_rect):
       print("collision")
       gravity_player += 1
       player_rect.y += gravity_player
    else:
        gravity_player += 1
        player_rect.y += gravity_player
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surface, player_rect)
        screen.blit(snail_surface, snail_rect)

    pygame.display.update()
    clock.tick(60)