import pygame
from person import Person
from wachs import Wachs
from candle import Candle
from rain import Raindrop
from wind import Wind
from platforms import Platform
from constants import *
import config
from PIL import Image
import time


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candle Run")
clock = pygame.time.Clock()

running = True
player_1 = Person()
candle = Candle(player_1)
time_2 = 0
timer = False
config.current_page = 0

pause_text = "PAUSE"

ghost_best = []
ghost_current = []
ghost_frame = 0
ghost_x = player_1.x
ghost_y = player_1.y

played_before = False


player_1.border = 3

jump_frame = 0
walk_frame = 0

green = (185, 145, 100)
brown = (144, 187, 66)

plaformscolor = [
    green,
    brown
]


#text stuff:########################################
pygame.font.init()
Antonio_font = pygame.font.Font('Antonio-Bold.ttf', 30)
Antonio_font_big = pygame.font.Font('Antonio-Bold.ttf', 80)
#end text stuff:#####################################

#create wachs:#######################################
wachs_1 = Wachs(0.1*WIDTH, 0.5*HEIGHT, 0, player_1, candle)
#end create wachs:###################################

#create rain:########################################
raindrops = []

width = 100
height = 200
for _ in range((width * height) // 1500):
    raindrops.append(Raindrop(int(0.5* WIDTH), int(0.5*HEIGHT), width, height, 0, player_1, candle, 0))
#end create rain#####################################

#create wind:########################################
windlist = []

width = WIDTH - 100
height = 800
for _ in range((width * height) // 3000):
    windlist.append(Wind(int(100), int(100), width, height, 0, player_1, 0, True))
#end create wind#####################################

#create Platform:####################################
#0 left:
platform_0_1 = Platform(0,0,50, HEIGHT, False, 0, 0)
#0 center:
platform_0_2 = Platform(50,HEIGHT - 100,WIDTH - 100, 100, False, 0, 0)
platform_0_3 = Platform(0,-50,WIDTH, 70, False, 0, 0)
platform_0_4 = Platform(200, 700, 200, 400, False, 0, 0)
platform_0_5 = Platform(800, 200, 200, 500, False, 0, 0)
platform_0_6 = Platform(500, 400, 200, 200, True, 0, -200)
#0 right:
platform_0_7 = Platform(WIDTH - 70,0,70, 0.5*HEIGHT, False, 0, 0)
plaform_0_8 = Platform(WIDTH - 70,0.7*HEIGHT,70, 0.4*HEIGHT, False, 0, 0)

#1 left:
platform_1_1 = Platform(0,0,70, 0.5*HEIGHT, False, 1, 0)
platform_1_2 = Platform(0,0.7*HEIGHT,70, 0.4*HEIGHT, False, 1, 0)
#1 center:
platform_1_3 = Platform(70, HEIGHT - 49, 0.5 * WIDTH, 50, False, 1, 0)
platform_1_4 = Platform(200, 700, 200, 100, False, 1, 0)
platform_1_5 = Platform(800, 200, 200, 100, False, 1, 0)
platform_1_6 = Platform(500, 400, 200, 100, False, 1, 0)
#1 right:
platform_1_7 = Platform(WIDTH - 40,0,40, 0.5*HEIGHT, False, 1, 0)
platform_1_8 = Platform(WIDTH - 40,0.85*HEIGHT,40, 0.4*HEIGHT, False, 1, 0)

#2 left:
platform_2_1 = Platform(0,0,60, 0.5*HEIGHT, False, 2, 0)
platform_2_2 = Platform(0,0.7*HEIGHT,60, 0.4*HEIGHT, False, 2, 0)
#2 center:
platform_2_3 = Platform(0, HEIGHT - 49, 0.5 * WIDTH, 50, False, 2, 0)
platform_2_4 = Platform(0.5 * WIDTH, HEIGHT - 99, 0.5 * WIDTH, 100, False, 2, 0)
platform_2_5 = Platform(200, 700, 200, 100, False, 2, 0)
platform_2_6 = Platform(800, 200, 200, 100, False, 2, 0)
platform_2_7 = Platform(500, 400, 200, 100, False, 2, 0)
#2 right:
#end create Platform:#################################

#background:#########################################
backgroundimage_nature = pygame.image.load("Pygame_Yuan_Mathieu/images/nature.jpg").convert()
backgroundimage_nature = pygame.transform.scale(backgroundimage_nature, (WIDTH, HEIGHT))
#end background######################################

player_1.change_character("redhat")

def ground():
    var_check_ground = vertical_bottom_y - 10
    while True:
        if vertical_left_x > 0 and vertical_right_x < WIDTH and 0 < var_check_ground < HEIGHT:
                color_bottom_left = screen.get_at((horizontal_left_x, int(var_check_ground)))
                color_bottom_right = screen.get_at((horizontal_right_x, int(var_check_ground)))
                if (color_bottom_left[:3] in plaformscolor) or (color_bottom_right[:3] in plaformscolor):
                    if player_1.ground != var_check_ground - player_1.border:
                        player_1.ground = var_check_ground - player_1.border
                    break
                else:
                    var_check_ground += 1
        elif (vertical_right_x >= WIDTH and 0 < var_check_ground < HEIGHT and WIDTH > horizontal_left_x > 0):
            color_bottom_left = screen.get_at((horizontal_left_x, int(var_check_ground)))
            if (color_bottom_left[:3] in plaformscolor):
                    player_1.ground = var_check_ground - player_1.border
                    break
            else:
                var_check_ground += 1
        
        elif vertical_left_x <= 0 and var_check_ground < HEIGHT:
            color_bottom_right = screen.get_at((horizontal_right_x, int(var_check_ground)))
            if (color_bottom_right[:3] in plaformscolor):
                    player_1.ground = var_check_ground - player_1.border
                    break
            else:
                var_check_ground += 1

        elif player_1.start:
            player_1.y -= 1
            player_1.vel_y = 0
            player_1.start = False
            break

        elif horizontal_left_x < WIDTH and horizontal_right_x > 0:
            player_1.ground = 2000
            break

def ceiling():
    var_check_ceiling = horizontal_top_y + 20
    while var_check_ceiling > 0 and True:
        if vertical_left_x > 0 and vertical_right_x < WIDTH:
            color_top_left = screen.get_at((vertical_left_x, int(var_check_ceiling)))
            color_top_right = screen.get_at((vertical_right_x, int(var_check_ceiling)))
            if (color_top_left[:3] in plaformscolor) or (color_top_right[:3] in plaformscolor):
                player_1.ceiling = var_check_ceiling
                break
            else:
                var_check_ceiling -= 1
        else:
            break

def check_bottom():
    if horizontal_left_x > 0 and horizontal_right_x < WIDTH and 0 < horizontal_bottom_y < HEIGHT:
        color_bottom_left = screen.get_at((horizontal_left_x, horizontal_bottom_y))
        color_bottom_right = screen.get_at((horizontal_right_x, horizontal_bottom_y))
        if (color_bottom_left[:3] not in plaformscolor) and (color_bottom_right[:3] not in plaformscolor): #fall down if not on ground
            check_fall(0)
        elif player_1.state != "jump":
            player_1.y = player_1.ground - player_1.height - 1

def check_fall(k):
    ground()
    if player_1.state != "jump":
        if horizontal_bottom_y + player_1.border < player_1.ground:
            player_1.vel_y += k * player_1.gravity  # Apply gravity
            player_1.y -= player_1.vel_y
        else:            
            player_1.y = player_1.ground - player_1.height - player_1.border
            player_1.vel_y = 0

def check_ceiling():
    if 0 < horizontal_right_x < WIDTH and 0 < horizontal_top_y < HEIGHT and 0 < horizontal_left_x < WIDTH:
            color_top_right = screen.get_at((horizontal_right_x, horizontal_top_y))
            color_top_left = screen.get_at((horizontal_left_x, horizontal_top_y))
            if color_top_right[:3] in plaformscolor or color_top_left[:3] in plaformscolor:
                ceiling()
                player_1.y = player_1.ceiling + player_1.border
                player_1.y += player_1.speed
                player_1.vel_y = 0  # Stop upward movement on collision 
    elif WIDTH >= horizontal_left_x > 0 and 0 < horizontal_top_y < HEIGHT:
            color_top_left = screen.get_at((horizontal_left_x, horizontal_top_y))
            if color_top_left[:3] in plaformscolor:
                player_1.y += player_1.speed
                player_1.vel_y = 0  # Stop upward movement on collision
    elif horizontal_left_x <= 0 and WIDTH > horizontal_right_x > 0 and 0 < horizontal_top_y < HEIGHT:
            color_top_right = screen.get_at((horizontal_right_x, horizontal_top_y))
            if color_top_right[:3] in plaformscolor:
                player_1.y += player_1.speed
                player_1.vel_y = 0  # Stop upward movement on collision$

def check_left():
    if vertical_left_x > 0 and vertical_right_x <= WIDTH and vertical_bottom_y < HEIGHT and vertical_top_y > 0:
            color_left_top = screen.get_at((vertical_left_x, vertical_top_y + 5))
            color_left_bottom = screen.get_at((vertical_left_x, vertical_bottom_y - 5))
            if color_left_top[:3] in plaformscolor or color_left_bottom[:3] in plaformscolor:
                player_1.collision_left = True
                if player_1.state == "jump" and right:
                    player_1.vel_y = 20
                else:
                    if right:
                        player_1.vel_x = player_1.speed
                    else:
                        player_1.vel_x = 0
            elif left:
                player_1.collision_left = False
                player_1.vel_x = -player_1.speed
            else:
                player_1.collision_left = False
    elif left:
            player_1.vel_x = -player_1.speed
        
def check_right():
        if vertical_right_x < WIDTH and player_1.x > 0 and player_1.y > 0 and vertical_bottom_y < HEIGHT:
            color_right_top = screen.get_at((vertical_right_x , vertical_top_y + 5))
            color_right_bottom = screen.get_at((vertical_right_x, vertical_bottom_y - 5))
            if color_right_top[:3] in plaformscolor or color_right_bottom[:3] in plaformscolor:
                player_1.collision_right = True
                player_1.wind_component = 0
                if player_1.state == "jump" and left:
                    player_1.vel_y = 20
                else:
                    if left:
                        player_1.vel_x = -player_1.speed
                    else:
                        player_1.vel_x = 0
            elif right:
                player_1.vel_x = player_1.speed
                player_1.collision_right = False
            else:
                player_1.collision_right = False
        elif right:
            player_1.vel_x = player_1.speed


def pause_function():
    if player_1.fail == False:
        global pause_text
        if pause_text == "PAUSE":
            pause_text = "RESUME"
            player_1.command = False
            timer = True
            for platform in Platform.instances:
                platform.v_y = 0
        else:
            pause_text = "PAUSE"
            player_1.command = True
            timer = False
            for platform in Platform.instances:
                platform.v_y = platform.v_y_default

def game_over():
    timer = False
    player_1.command = False
    player_1.fail = True
    game_over_text = Antonio_font_big.render("GAME OVER", True, (255, 0, 0))
    center_text = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, center_text)
    candle.percentageheight = 0

def reset_to_initial():
    timer = False
    success = False
    for w in Wachs.instances:
        w.show = True
    for platform in Platform.instances:
        platform.y = platform.y_default
    candle.percentageheight = 100
    ground()
    ghost_current = []
    ghost_frame = 0
    time_2 = 0
    player_1.default()
    pause_text = "PAUSE"
    config.current_page = 0


while running:
    start = time.perf_counter()
    horizontal_left_x = int(player_1.x)
    horizontal_bottom_y = int(player_1.y + player_1.height + player_1.border)
    horizontal_right_x = int(player_1.x + player_1.width + player_1.border)
    horizontal_top_y = int(player_1.y - 1 - player_1.border)

    vertical_left_x = int(player_1.x - 2 - player_1.border)
    vertical_top_y = int(player_1.y - player_1.border)
    vertical_bottom_y = int(player_1.y + player_1.height + player_1.border)
    vertical_right_x = int(player_1.x + player_1.width + 1 + player_1.border)


    img = Image.open(f"Pygame_Yuan_Mathieu/png_{player_1.character}/Run (1).png")   # no leading slash
    width, height = img.size
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: #start timer when any key is pressed
            if time_2 == 0:
                timer = True
                time_2 = pygame.time.get_ticks()
        if (player_1.command == True) and (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            player_1.jump()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_rect.collidepoint(event.pos):
                pause_function()
                timer = False if pause_text == "RESUME" else True
            elif restart_rect.collidepoint(event.pos):
                reset_to_initial()
            elif settings_rect.collidepoint(event.pos):
                if player_1.settings_page == False:
                    player_1.settings_page = True
                else:
                    player_1.settings_page = False
                    player_1.start = True
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
        check_left()
        check_right()

        #check top left and top right side of the person:
        check_ceiling()
        check_fall(1)
      
        if player_1.state != "jump":
            #check bottom left and right side of the person:
            check_bottom()
                    
        if timer == True:
            time_2 += 1
            candle.percentageheight -= 0.02
            candle.percentageheight = round(candle.percentageheight, 2)

        if timer == True and player_1.command == True:
            ghost_current.append((player_1.x, player_1.y, config.current_page))
        
        
    player_1.update(horizontal_right_x)

    for raindrop in raindrops:
        raindrop.update()

    for wind in windlist:
        wind.update()

    for wind in windlist:
        wind.update()
    
    for platform in Platform.instances:
        platform.update()
    
    """for key in Raindrop.instances:
        Raindrop.instances[key] = False"""
    #draw#####################################################
    #screen.fill("black")

    

    if player_1.y > HEIGHT:
        game_over()
    
    if player_1.success == False and player_1.fail == False:
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


        
        widthbefore = player_1.width

        image = pygame.image.load(player_1.pngpath).convert_alpha()
        width = image.get_width()
        height = image.get_height()

        player_1.width = 100 * (width / height)
        if player_1.width > widthbefore:
            difference = player_1.width - widthbefore 
        if vertical_left_x - difference > 0 and vertical_bottom_y < HEIGHT and vertical_top_y > 0:
            color_left_top = screen.get_at((int(vertical_left_x - difference), vertical_top_y + 5))
            color_left_bottom = screen.get_at((int(vertical_left_x - difference), vertical_bottom_y - 5))
            if color_left_top[:3] in plaformscolor or color_left_bottom[:3] in plaformscolor:
                player_1.leftwall = True
            else:
                player_1.leftwall = False

        
        if player_1.leftwall == False:
            player_1.x = player_1.x - player_1.width + widthbefore

        
        screen.blit(backgroundimage_nature, (0, 0))

        draw = player_1.draw(screen)

        for raindrop in raindrops:
            draw = raindrop.draw(screen)
        
        for wind in windlist:
            draw = wind.draw(screen)
            config.check_wind == True

        for platform in Platform.instances:
            draw = platform.draw(screen)

    if candle.percentageheight <= 0:
         game_over()


    #Wachs:
    for w in Wachs.instances:
        draw = w.draw(screen)

    draw = candle.draw(screen)

    if player_1.success == True:
        played_before = True
        ghost_frame = 0
        if len(ghost_current) != 0:
            if ghost_best != [] and len(ghost_current) < len(ghost_best):
                ghost_best = ghost_current
            elif len(ghost_best) == 0:
                ghost_best = ghost_current
            ghost_current = []

        success = Antonio_font_big.render("YOU MADE IT", True, (0, 255, 0))
        center_text = success.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(success, center_text)

    
    if player_1.settings_page == True:
        screen.fill("black")

    #navigation bar:
    pause = Antonio_font.render(pause_text, True, (0, 0, 0))
    pause_rect = pause.get_rect(topright=(WIDTH - 30, 0))

    restart = Antonio_font.render("RESTART", True, (0, 0, 0))
    restart_rect = restart.get_rect(topright=(WIDTH - pause_rect.width - 60, 0))

    settings = Antonio_font.render("SETTINGS", True, (0, 0, 0))
    settings_rect = settings.get_rect(topright=(WIDTH - pause_rect.width - restart_rect.width - 90, 0))

    recttop = pygame.Rect(WIDTH - pause_rect.width - restart_rect.width - settings_rect.width - 120, 0, 500, 50)
    
    pygame.draw.rect(screen, (255,255,255), recttop)
    screen.blit(settings, settings_rect)
    screen.blit(restart, restart_rect)
    screen.blit(pause, pause_rect)

    

    pygame.display.flip()

    end = time.perf_counter()
    frame_time = end - start
    #print(f"Frame took {frame_time:.6f} seconds")

    clock.tick(60)

pygame.quit()