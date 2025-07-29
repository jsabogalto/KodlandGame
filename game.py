import pygame
from random import randint
from sys import exit


def score_time():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    return current_time

def show_screen_text(text, x, y):
    menu_surface = test_font.render(f"{text}", False, "Black")
    menu_rect = menu_surface.get_rect(center = (x, y))
    return menu_surface, menu_rect


def player_animation():
    global player_surface, player_index
    
    if player_rect.bottom < 300: 
        player_surface = player_surface_jump 
    else: 
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surface = player_walk[int(player_index)]
def fly_animation():
    global fly_surface, fly_index
    fly_index += 0.1
    if fly_index >= len(fly_fling):fly_index = 0
    fly_surface = fly_fling[int(fly_index)]

def snail_animation():
    global snail_surface, snail_index
    snail_index += 0.1
    if snail_index >= len(snail_walk):snail_index = 0
    snail_surface = snail_walk[int(snail_index)]

def obstacle_movement(enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5

            if enemy_rect.bottom == 300:
                snail_animation()
                screen.blit(snail_surface, enemy_rect)
            else:
                fly_animation()
                screen.blit(fly_surface, enemy_rect)


        enemy_list = [enemy for enemy in enemy_list if enemy.x > - 100]
        return enemy_list
    
    else:
        return []
    
def collisions(player, enemies):
    if enemies:
        for enemy_rect in enemies:
            if player.colliderect(enemy_rect): return False
    return True

#inicio y configuracion de pantalla principal
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Juego de Jonathan")
clock = pygame.time.Clock()
#texto 
test_font = pygame.font.Font("public/Pixeltype.ttf", 50)
#configuracion del mapa
sky_surface = pygame.image.load("public/background.png").convert()
ground_surface = pygame.image.load("public/ground.png").convert()
#jugador
player_surface_walk_1 = pygame.image.load("public/Player/walk.png").convert_alpha()
player_surface_walk_2 = pygame.image.load("public/Player/walk_2.png").convert_alpha()
player_walk = [player_surface_walk_1, player_surface_walk_2]
player_index = 0
player_surface_jump = pygame.image.load("public/Player/jump.png").convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0
bullets = []
#primer enemigo
snail_surface_1 = pygame.image.load("public/snail/snail1.png").convert_alpha()
snail_surface_2 = pygame.image.load("public/snail/snail2.png").convert_alpha()
snail_walk = [snail_surface_1, snail_surface_2]
snail_index = 0
snail_surface = snail_walk[snail_index]
snail_rect = snail_surface.get_rect(bottomright = (600, 300))
#sgundo enimigo
fly_surface_1 = pygame.image.load("public/Fly/Fly1.png").convert_alpha()
fly_surface_2 = pygame.image.load("public/Fly/Fly2.png").convert_alpha()
fly_fling = [fly_surface_1, fly_surface_2]
fly_index = 0
fly_surface = fly_fling[fly_index]
fly_rect = fly_surface.get_rect(bottomright = (600, 200))

enemy_list = []
#score
# score_surface = test_font.render("Juego", False, "Green")
# score_rect = score_surface.get_rect(center = (400, 50))
#gravity for player
gravity_player = 0
#game active
game_active = True
#start time
start_time = 0

#main menu
menu_surface = test_font.render("presiona espacio para jugar", False, "Black")
menu_rect = menu_surface.get_rect(center = (400, 300))
menu_image = pygame.image.load("public/Player/player_stand.png").convert_alpha()
manu_image_rect = menu_image.get_rect(center = (400, 200))
#`obstacul`os
obstacle_time = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_time, 900)
#records
records = []

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
        
        if event.type == pygame.KEYDOWN and game_active == False:
            if event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)
        
        if event.type == obstacle_time and game_active:
            if randint(0, 2):
                enemy_list.append(snail_surface.get_rect(bottomright = (randint(900, 1100), 300)))
            else:
                enemy_list.append(fly_surface.get_rect(bottomright = (randint(900, 1100), 200)))
            print("test")
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # disparar con F
                bullet = pygame.Rect(player_rect.right, player_rect.centery - 5, 10, 10)
                bullets.append(bullet)

    if game_active:
        #dibujar por pantalla
        #actualizar los obj1etos
        screen.blit(ground_surface, (0, 300))
        screen.blit(sky_surface, (0, 0))
        
        score = score_time()
        score_surface = test_font.render(f"Tu puntaje: {score}", False, "Black")
        score_rect = score_surface.get_rect(center = (400, 50))
        screen.blit(score_surface, score_rect)
        records.append(score)
        # snail_rect.x -= 5
        # if snail_rect.right <= 0 : snail_rect.left = 800
        #obtacle movement
        enemy_list = obstacle_movement(enemy_list)

        for bullet in bullets:
            bullet.x += 10  # velocidad
        bullets = [b for b in bullets if b.x < 800] 
        
        #surface 
        gravity_player += 1
        player_rect.y += gravity_player
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)
        for bullet in bullets:
            for enemy in enemy_list:
                if bullet.colliderect(enemy):
                    if enemy in enemy_list:
                        enemy_list.remove(enemy)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    break  # salir del loop interno
        #collisions
        game_active = collisions(player_rect, enemy_list)

        for bullet in bullets:
            pygame.draw.rect(screen, (0, 0, 0), bullet)


    else:
        screen.fill((94,129,162))

        records_surface = test_font.render(f"Tus puntajes: {records}", False, "Black")
        records_rect = score_surface.get_rect(center = (400, 200))
        screen.blit(records_surface, records_rect)
        menu_surface, menu_rect = show_screen_text("presiona espacio para empezar", x=400, y=300) 
        enemy_list.clear()
        screen.blit(menu_surface, menu_rect)
        screen.blit(menu_image, manu_image_rect)
        

    pygame.display.update()
    clock.tick(60)