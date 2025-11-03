import pygame
import math
import random
from person import Person
from constants import *
import config

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
player_1 = Person()
time = 0
timer = False
config.current_page = 0
pause_text = "PAUSE"
settings_page = False

ghost_best = []
ghost_current = []
ghost_frame = 0
ghost_x = player_1.x
ghost_y = player_1.y

played_before = False



#text stuff:########################################
pygame.font.init()
Antonio_font = pygame.font.Font('Antonio-Bold.ttf', 30)
Antonio_font_big = pygame.font.Font('Antonio-Bold.ttf', 80)
#end text stuff:#####################################

def ground():
    var_check_ground = player_1.y + player_1.height
    while var_check_ground < HEIGHT and True:
        if player_1.x > 0 and player_1.x + player_1.width < WIDTH:
            color_bottom_left = screen.get_at((player_1.x, int(var_check_ground)))
            color_bottom_right = screen.get_at((player_1.x + player_1.width, int(var_check_ground)))
            if (color_bottom_left[:3] == (255,255,255)) or (color_bottom_right[:3] == (255,255,255)):
                player_1.ground = var_check_ground - 1
                #player_1.y =player_1.ground - player_1.height
                break
            else:
                var_check_ground += 1
        else:
            break

def check_fall():
    ground()
    if player_1.is_jumping == False:
        if player_1.y + player_1.height < player_1.ground:
            player_1.vel_y += player_1.gravity  # Apply gravity
            player_1.y -= player_1.vel_y
        else:
            player_1.y = player_1.ground - player_1.height - 1
            player_1.vel_y = 0

def pause_function():
    global pause_text
    if pause_text == "PAUSE":
        pause_text = "RESUME"
        player_1.command = False
        timer = True
    else:
        pause_text = "PAUSE"
        player_1.command = True
        timer = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: #start timer when any key is pressed
            if time == 0:
                timer = True
                time = pygame.time.get_ticks()
        if (player_1.command == True) and (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            player_1.jump()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_rect.collidepoint(event.pos):
                pause_function()
                timer = False if pause_text == "RESUME" else True
            elif restart_rect.collidepoint(event.pos):
                timer = False
                success = False
                ghost_current = []
                ghost_frame = 0
                time = 0
                player_1 = Person()
                pause_text = "PAUSE"
                config.current_page = 0
            elif settings_rect.collidepoint(event.pos):
                settings_page = True if settings_page == False else False
                #timer = True if pause_text == "RESUME" else True
                pause_function()
    
    if player_1.command == True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            right = True
        else:
            right = False

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            left = True
        else:
            left = False

        if keys[pygame.K_DOWN]:
            player_1.gravity = -3
            
        elif keys[pygame.K_UP]:
            player_1.gravity = -0.5
        else:
            player_1.gravity = -1.5
        
        player_1.vel_x = 0
        #check left and right side of the person:
        if player_1.x + player_1.width + 1 <= WIDTH and player_1.x > 0 and player_1.y > 0:
            color_right_top = screen.get_at((int(player_1.x) + int(player_1.width), int(player_1.y)))
            color_right_bottom = screen.get_at((int(player_1.x) + int(player_1.width), int(player_1.y) + int(player_1.height) - 1))
            if color_right_top[:3] == (255, 255, 255) or color_right_bottom[:3] == (255, 255, 255):
                if player_1.is_jumping == True and left:
                    player_1.vel_y = 20
                else:
                    if left:
                        player_1.vel_x = -player_1.speed
                    else:
                        player_1.vel_x = 0
            elif right:
                player_1.vel_x = player_1.speed
        elif right:
            player_1.vel_x = player_1.speed

        if player_1.x - 3 > 0 and player_1.x + player_1.width + 2 < WIDTH:
            color_left_top = screen.get_at((int(player_1.x) - 3, int(player_1.y)))
            color_left_bottom = screen.get_at((int(player_1.x) - 3, int(player_1.y) + int(player_1.height)))
            if color_left_top[:3] == (255, 255, 255) or color_left_bottom[:3] == (255, 255, 255):
                if player_1.is_jumping == True and right:
                    player_1.vel_y = 20
                else:
                    if right:
                        player_1.vel_x = player_1.speed
                    else:
                        player_1.vel_x = 0
            elif left:
                player_1.vel_x = -player_1.speed
        elif left:
            player_1.vel_x = -player_1.speed

        #check top left and top right side of the person:
        if player_1.x > 0 and player_1.x + player_1.width < WIDTH:
            color_top_right = screen.get_at((int(player_1.x) + int(player_1.width), int(player_1.y) - 2))
            color_top_left = screen.get_at((int(player_1.x), int(player_1.y) - 2))
            if color_top_right[:3] == (255, 255, 255) or color_top_left[:3] == (255, 255, 255):
                player_1.y += player_1.speed
                player_1.vel_y = 0  # Stop upward movement upon collision
        elif player_1.x < WIDTH and player_1.x > 0:
            color_top_left = screen.get_at((int(player_1.x), int(player_1.y) - 2))
            if color_top_left[:3] == (255, 255, 255):
                player_1.y += player_1.speed
                player_1.vel_y = 0  # Stop upward movement upon collision
        
        if player_1.is_jumping == True:
            check_fall()
        #check bottom left and right side of the person:
        if player_1.x > 0 and player_1.x + player_1.width < WIDTH:
            color_bottom_left = screen.get_at((int(player_1.x), int(player_1.y + player_1.height + 2)))
            color_bottom_right = screen.get_at((int(player_1.x + player_1.width), int(player_1.y + player_1.height + 2)))
            if (color_bottom_left[:3] == (0,0,0)) and (color_bottom_right[:3] == (0,0,0)): #fall down if not on ground
                check_fall()
            elif player_1.is_jumping == False:
                player_1.y = player_1.ground - player_1.height - 1
        
        
        if timer == True:
            time += 1
            player_1.candle_percentage -= 0.01
            player_1.candle_percentage = round(player_1.candle_percentage, 2)

        if timer == True and player_1.command == True:
            ghost_current.append((player_1.x, player_1.y, config.current_page))


    player_1.update()

    #draw#####################################################
    screen.fill("black")

    #navigation bar:
    recttop = pygame.Rect(0, 0, WIDTH, 50)
    pygame.draw.rect(screen, (255,255,255), recttop)




    

    #pause = Antonio_font.render("PAUSE", True, (0,0, 0))
    #screen.blit(pause, (WIDTH - 150,0))

    pause = Antonio_font.render(pause_text, True, (0, 0, 0))
    pause_rect = pause.get_rect(topleft=(WIDTH - 150, 0))
    screen.blit(pause, pause_rect)

    restart = Antonio_font.render("RESTART", True, (0, 0, 0))
    restart_rect = restart.get_rect(topleft=(WIDTH - 300, 0))
    screen.blit(restart, restart_rect)

    
    
    if player_1.success == False:
        # draw ghost:
        if played_before == True:
            if timer == True:
                if len(ghost_best) > ghost_frame + 1:
                    ghost_frame += 1
                    ghost_x, ghost_y, ghost_current_page = ghost_best[ghost_frame]
                    if ghost_current_page == config.current_page:
                        ghost_rect = pygame.Rect(ghost_x, ghost_y, player_1.width, player_1.height)
                        pygame.draw.rect(screen, (100,100,100), ghost_rect)
            elif ghost_frame != 0:
                ghost_rect = pygame.Rect(ghost_x, ghost_y, player_1.width, player_1.height)
                pygame.draw.rect(screen, (100,100,100), ghost_rect)
        draw = player_1.draw(screen)

        candle_percentage = Antonio_font.render(str(player_1.candle_percentage)+"%", True, (percentage_r, percentage_g, percentage_b))
        screen.blit(candle_percentage, (50,50))

        for i in range (len(config.platforms[config.current_page])):
            rect = pygame.Rect(config.platforms[config.current_page][i][0], config.platforms[config.current_page][i][1], config.platforms[config.current_page][i][2], config.platforms[config.current_page][i][3])
            pygame.draw.rect(screen, "white", rect)
    
    
    if player_1.candle_percentage == 0:
        timer = False
        player_1.command = False
        game_over = Antonio_font_big.render("GAME OVER", True, (255, 0, 0))
        center_text = success.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over, center_text)
    elif player_1.candle_percentage <= 10:            
        percentage_r = 255
        percentage_g = 0
        percentage_b = 0

    if player_1.success == True:
        played_before = True
        ghost_frame = 0
        if len(ghost_current) != 0:
            if ghost_best != [] and len(ghost_current) < len(ghost_best):
                ghost_best = ghost_current
            elif len(ghost_best) == 0:
                ghost_best = ghost_current
            ghost_current = []
       
        #success = Antonio_font_big.render("YOU MADE IT", True, (255, 0, 0))
        #screen.blit(success, (0.5*WIDTH,0.5*HEIGHT))
        success = Antonio_font_big.render("YOU MADE IT", True, (0, 255, 0))
        center_text = success.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(success, center_text)
    
    

    if settings_page == True:
        screen.fill("black")


    settings = Antonio_font.render("SETTINGS", True, (0, 0, 0) if settings_page == False else (255,255,255))
    settings_rect = settings.get_rect(topleft=(50, 0))
    screen.blit(settings, settings_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()