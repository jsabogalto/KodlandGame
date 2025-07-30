import pygame
from random import randint
from sys import exit


def score_time():
    """
    mostrar el tiempo que se lleva jugando
    """
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    return current_time

def show_screen_text(text, x, y):
    """
    mostrar texto
    args: texto a renderizar y sus coordenadas
    """
    menu_surface = test_font.render(f"{text}", False, "Black")
    menu_rect = menu_surface.get_rect(center = (x, y))
    return menu_surface, menu_rect


def player_animation():
    """
    transicion del movimiento del jugador
    """
    global player_surface, player_index
    
    if player_rect.bottom < 300: 
        player_surface = player_surface_jump 
    else: 
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surface = player_walk[int(player_index)]

def fly_animation():
    """anima el vuelo de la mosca"""
    global fly_surface, fly_index
    fly_index += 0.1
    if fly_index >= len(fly_fling):fly_index = 0
    fly_surface = fly_fling[int(fly_index)]

def snail_animation():
    """anima el movimiento de la calabaza"""
    global snail_surface, snail_index
    snail_index += 0.1
    if snail_index >= len(snail_walk):snail_index = 0
    snail_surface = snail_walk[int(snail_index)]

def dragon_animation():
    """anima el movimiento del dragon"""
    global dragon_surface, dragon_index
    dragon_index += 0.1
    if dragon_index >= len(dragon_walk):dragon_index = 0
    dragon_surface = dragon_walk[int(snail_index)]

def obstacle_movement(enemy_list):
    """
    renderizamos la lista de enemigos y llamamos a sus animaciones si no detecta un enemigo envia una lista vacia 
    """
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 6
            if enemy_rect.bottom == 301:
                enemy_rect.x -= 7
                dragon_animation()
                screen.blit(dragon_surface, enemy_rect)
            elif enemy_rect.bottom == 300:
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
    """detectamos colisiones entre el jugador y los enemigos"""
    if enemies:
        for enemy_rect in enemies:
            if player.colliderect(enemy_rect): 
                return True
    return False


#inicio y configuracion de pantalla principal
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Juego de Jonathan para ")
clock = pygame.time.Clock()
#texto 
test_font = pygame.font.Font("public/Pixeltype.ttf", 50)
#configuracion del mapa
sky_surface = pygame.image.load("public/background.png").convert()
ground_surface = pygame.image.load("public/ground.png").convert()
#jugador
player_surface_walk_1 = pygame.image.load("public/Player/walk.png").convert_alpha()
player_surface_walk_2 = pygame.image.load("public/Player/walk_2.png").convert_alpha()
player_surface_hurt = pygame.image.load("public/Player/hurts.png").convert_alpha()
player_walk = [player_surface_walk_1, player_surface_walk_2]
player_index = 0
lifes = 3
last_hit_time = 0
invulnerable_time = 1000 
player_surface_jump = pygame.image.load("public/Player/jump.png").convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0
#tokens para eliminar enemigos
bullets_surface = pygame.image.load("public/Player/hacha.png").convert_alpha()
bullets_list = []
token_bullets = 10
token_visible = False
token_surface = pygame.image.load("public/Player/hacha.png").convert_alpha()
token_rect = token_surface.get_rect(center=(randint(200, 600), 250))
enemy_killed_count = 0

#primer enemigo
snail_surface_1 = pygame.image.load("public/calabaza/calabaza1.png").convert_alpha()
snail_surface_2 = pygame.image.load("public/calabaza/calabaza2.png").convert_alpha()
snail_surface_3 = pygame.image.load("public/calabaza/calabaza3.png").convert_alpha()
snail_surface_4 = pygame.image.load("public/calabaza/calabaza4.png").convert_alpha()
#imagenes para animarlo
snail_walk = [snail_surface_1, snail_surface_2, snail_surface_3, snail_surface_4]
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
#tercer enmigo
dragon_surface_1 = pygame.image.load("public/dragon/dragon1.png").convert_alpha()
dragon_surface_2 = pygame.image.load("public/dragon/dragon2.png").convert_alpha()
dragon_surface_3 = pygame.image.load("public/dragon/dragon3.png").convert_alpha()
dragon_surface_4 = pygame.image.load("public/dragon/dragon4.png").convert_alpha()
dragon_walk = [dragon_surface_1, dragon_surface_2, dragon_surface_3, dragon_surface_4]
dragon_index = 0
dragon_surface = snail_walk[snail_index]
dragon_rect = snail_surface.get_rect(bottomright = (1000, 301))
enemy_list = []
#gravedad para el jugador
gravity_player = 0
#juego activo
game_active = False
#tiempo para el score
start_time = 0

#main menu
menu_surface = test_font.render("presiona espacio para jugar", False, "Black")
menu_rect = menu_surface.get_rect(center = (400, 300))
menu_image = pygame.image.load("public/Player/player_stand.png").convert_alpha()
manu_image_rect = menu_image.get_rect(center = (400, 200))
#obstaculos
obstacle_time = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_time, 900)
#records
score = 0


#inicio del juego
while(True):
    #obtener los eventos
    for event in pygame.event.get():
        #detecta si cerramos la ventana y finaliza
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
        #capturar la posicion del mouse para posicionar objetos
        if event.type == pygame.MOUSEMOTION:
            print(event.pos)
        #tecla espacio la cual recibe 20px de salto
        if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
            if event.key == pygame.K_SPACE:
                gravity_player = -20
        #inicio de la siguiente ronda
        if event.type == pygame.KEYDOWN and game_active == False:
            if event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                dragon_rect.left = 1000
                start_time = int(pygame.time.get_ticks() / 1000)
        # enemigos que aparecen al azar con random
        if event.type == obstacle_time and game_active:
            if randint(0, 2):
                enemy_list.append(snail_surface.get_rect(bottomright = (randint(900, 1100), 300)))
            elif randint(0, 3):
                enemy_list.append(dragon_surface.get_rect(bottomright = (randint(900, 1100), 301)))
            else:
                enemy_list.append(fly_surface.get_rect(bottomright = (randint(900, 1100), 200)))
            print("test")
        #uso del token hachas para eliminar enemigos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and token_bullets > 0:
                bullet_rect = bullets_surface.get_rect(midleft=(player_rect.right, player_rect.centery))
                bullets_list.append(bullet_rect)     
                token_bullets -= 1   

    if game_active:
        #dibujar por pantalla
        #actualizar los obj1etos
        screen.blit(ground_surface, (0, 300))
        screen.blit(sky_surface, (0, 0))
        
        #puntaje del jugador
        score = score_time()
        score_surface = test_font.render(f"Tu puntaje: {score}", False, "Black")
        score_rect = score_surface.get_rect(center = (400, 50))
        screen.blit(score_surface, score_rect)
        #vidas
        lifes_surface, lifes_rect = show_screen_text(f"Vidas: {lifes}", x=100, y=50)
        screen.blit(lifes_surface, lifes_rect)

        enemy_list = obstacle_movement(enemy_list)

        #velocidad de las hachas
        for bullet in bullets_list:
            bullet.x += 7
        bullets_list = [b for b in bullets_list if b.x < 800]
        
        #renderizar el jugador
        gravity_player += 1
        player_rect.y += gravity_player
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)


        #colision con los enemigos y resta de vidas si hay colision
        current_time = pygame.time.get_ticks()
        #damos tiempo ya que como vamos a 60 fps el juego por una colision capta 60 entonces usamos get_ticks par obtener los milisegundos y dar un tiempo al jugador para que pueda continuar 
        if collisions(player_rect, enemy_list):
            if current_time - last_hit_time > invulnerable_time:
                lifes -= 1
                last_hit_time = current_time
                screen.blit(player_surface_hurt, player_rect)
                pygame.display.update()
                pygame.time.delay(150)
                if lifes < 2 and not token_visible:
                    token_visible = True
                    token_rect.center = (600, 250)
              # reubicar el token
        
        if lifes == 0:
            game_active = False

        #renderizamos las hachas
        for bullet in bullets_list:
            screen.blit(bullets_surface, bullet)
        
        #verificamos colisiones de tokens de hachas con enemigos si es asi anadimos una unidad al contador de enemigos eliminados
        for bullet in bullets_list:
            for enemy in enemy_list:
                if bullet.colliderect(enemy):
                    if enemy in enemy_list:
                        enemy_list.remove(enemy)
                        enemy_killed_count += 1 
                    if bullet in bullets_list:
                        bullets_list.remove(bullet)
                    break

        #verificamos los enemigos eliminados si son mas de 5 se muestra un token el cual el jugador debera colisionar con el para que la variable de bullets aumente 5 y pueda disparar mas hachas
        if enemy_killed_count >= 5 and not token_visible:
            token_visible = True
            token_rect.center = (600, 250)
              # reubicar el token
            enemy_killed_count = 0

        #mostrar el token
        if token_visible:
            token_rect.x -= 5
            screen.blit(token_surface, token_rect)
            if player_rect.colliderect(token_rect):
                token_bullets = 5
                token_visible = False
        #mostrar las hachas que le quedan al jugador
        len_hachas_surface, len_hachas_rect = show_screen_text(f"Hachas: {token_bullets}", x=700, y=50)
        screen.blit(len_hachas_surface, len_hachas_rect)
    else:
        #cuando el juego no esta activo se muestra el menu juego
        screen.fill((94,129,162))

        if score > 1:
            records_surface = test_font.render(f"Tu puntaje fue: {score}", False, "Black")
            records_rect = score_surface.get_rect(center = (400, 200))
            screen.blit(records_surface, records_rect)
        else:
            menu_inicio, menu_rect_inicio = show_screen_text("Bienvenido a Kodland Game Boy", x=400, y=100)
            screen.blit(menu_inicio, menu_rect_inicio)
            menu_inicio, menu_rect_inicio = show_screen_text("tienes tres vidas y 10 hachas puedes eliminar", x=400, y=150)
            screen.blit(menu_inicio, menu_rect_inicio)
            menu_inicio, menu_rect_inicio = show_screen_text("enemigos con ellas y obtener mas para eliminar", x=400, y=200)
            screen.blit(menu_inicio, menu_rect_inicio)
            menu_inicio, menu_rect_inicio = show_screen_text(" mas enemigos buena suerte!", x=400, y=250)
            screen.blit(menu_inicio, menu_rect_inicio)

        menu_surface, menu_rect = show_screen_text("presiona espacio para empezar", x=400, y=300) 
        enemy_list.clear()
        screen.blit(menu_surface, menu_rect)
        token_bullets = 10
        lifes = 3

    pygame.display.update()
    clock.tick(60)