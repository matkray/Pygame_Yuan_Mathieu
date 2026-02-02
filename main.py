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
from sound_manager import play_jump_sound, play_landing_sound
from settings import render_settings, handle_settings_click, handle_settings_drag

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candle Run")
clock = pygame.time.Clock()

# Backdrop themes system
from themes import BACKDROP_THEMES, get_platform_colors

def create_gradient_background(width, height, top_color, bottom_color):
    surface = pygame.Surface((width, height))
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    return surface

def get_background_surface(theme_name):
    theme = BACKDROP_THEMES[theme_name]
    if theme["type"] == "image":
        bg = pygame.image.load(theme["background"]).convert()
        return pygame.transform.scale(bg, (WIDTH, HEIGHT))
    else:
        return create_gradient_background(WIDTH, HEIGHT, theme["top_color"], theme["bottom_color"])

running = True
player_1 = Person()
candle = Candle(player_1)
time_2 = 0
timer = False
config.current_page = 8

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

# Platform colors will be set dynamically based on backdrop theme
platformscolor = get_platform_colors(config.current_backdrop)

#text stuff:########################################
pygame.font.init()
Antonio_font = pygame.font.Font('Antonio-Bold.ttf', 30)
Antonio_font_big = pygame.font.Font('Antonio-Bold.ttf', 80)
#end text stuff:#####################################

#create wachs:#######################################
wachs_1_1 = Wachs(200, HEIGHT - 500 - 40, 1, player_1, candle)

wachs_2_1 = Wachs((WIDTH-100) // 3, HEIGHT - 40, 2, player_1, candle)
wachs_2_2 = Wachs((WIDTH-100) // 3 * 2, HEIGHT - 40, 2, player_1, candle)
wachs_2_3 = Wachs(WIDTH - 100, HEIGHT - 40, 2, player_1, candle)

wachs_3_1 = Wachs(750, 40, 3, player_1, candle)

wachs_4_1 = Wachs(1100, 100, 4, player_1, candle)

wachs_5_1 = Wachs(WIDTH - 150, HEIGHT - 200, 5, player_1, candle)

wachs_6_1 = Wachs(400, HEIGHT - 250, 6, player_1, candle)

wachs_8_1 = Wachs(WIDTH // 4 * 3 , HEIGHT // 2, 8, player_1, candle, 250, 250, True)

#end create wachs:###################################

#create rain:########################################
raindrops = []

raindrop_0_1_x = 300
raindrop_0_1_y = HEIGHT - 100
raindrop_0_1_width = 100
raindrop_0_1_height = 100
for _ in range((raindrop_0_1_width * raindrop_0_1_height) // 1500):
    raindrops.append(Raindrop(raindrop_0_1_x, raindrop_0_1_y, raindrop_0_1_width, raindrop_0_1_height, 0, player_1, candle, 0))

raindrop_0_2_x = 850
raindrop_0_2_y = HEIGHT - 100
raindrop_0_2_width = 250
raindrop_0_2_height = 100
for _ in range((raindrop_0_2_width * raindrop_0_2_height) // 1500):
    raindrops.append(Raindrop(raindrop_0_2_x, raindrop_0_2_y, raindrop_0_2_width, raindrop_0_2_height, 0, player_1, candle, 1))

raindrop_3_1_x = 350
raindrop_3_1_y = HEIGHT - 100
raindrop_3_1_width = 200
raindrop_3_1_height = 100
for _ in range((raindrop_3_1_width * raindrop_3_1_height) // 1500):
    raindrops.append(Raindrop(raindrop_3_1_x, raindrop_3_1_y, raindrop_3_1_width, raindrop_3_1_height, 3, player_1, candle, 2))

raindrop_3_2_x = 1000
raindrop_3_2_y = HEIGHT - 300
raindrop_3_2_width = 200
raindrop_3_2_height = 300
for _ in range((raindrop_3_2_width * raindrop_3_2_height) // 1500):
    raindrops.append(Raindrop(raindrop_3_2_x, raindrop_3_2_y, raindrop_3_2_width, raindrop_3_2_height, 3, player_1, candle, 3))

raindrop_4_1_x = 550
raindrop_4_1_y = HEIGHT - 350
raindrop_4_1_width = 150
raindrop_4_1_height = 100
for _ in range((raindrop_4_1_width * raindrop_4_1_height) // 1500):
    raindrops.append(Raindrop(raindrop_4_1_x, raindrop_4_1_y, raindrop_4_1_width, raindrop_4_1_height, 4, player_1, candle, 0))

raindrop_5_1_x = 900
raindrop_5_1_y = HEIGHT - 250
raindrop_5_1_width = 250
raindrop_5_1_height = 100
for _ in range((raindrop_5_1_width * raindrop_5_1_height) // 1500):
    raindrops.append(Raindrop(raindrop_5_1_x, raindrop_5_1_y, raindrop_5_1_width, raindrop_5_1_height, 5, player_1, candle, 0))

raindrop_6_1_x = 850
raindrop_6_1_y = HEIGHT - 100
raindrop_6_1_width = 750
raindrop_6_1_height = 100
for _ in range((raindrop_6_1_width * raindrop_6_1_height) // 1500):
    raindrops.append(Raindrop(raindrop_6_1_x, raindrop_6_1_y, raindrop_6_1_width, raindrop_6_1_height, 6, player_1, candle, 0))

raindrop_7_1_x = 100
raindrop_7_1_y = HEIGHT - 100
raindrop_7_1_width = 350
raindrop_7_1_height = 100
for _ in range((raindrop_7_1_width * raindrop_7_1_height) // 1500):
    raindrops.append(Raindrop(raindrop_7_1_x, raindrop_7_1_y, raindrop_7_1_width, raindrop_7_1_height, 7, player_1, candle, 0))

raindrop_7_2_x = 750
raindrop_7_2_y = HEIGHT - 100
raindrop_7_2_width = 300
raindrop_7_2_height = 100
for _ in range((raindrop_7_2_width * raindrop_7_2_height) // 1500):
    raindrops.append(Raindrop(raindrop_7_2_x, raindrop_7_2_y, raindrop_7_2_width, raindrop_7_2_height, 7, player_1, candle, 0))


#end create rain#####################################

#create wind:########################################
windlist = []

wind_0_1_x = 1100
wind_0_1_y = HEIGHT - 450
wind_0_1_width = 300
wind_0_1_height = 100
for _ in range((wind_0_1_width * wind_0_1_height) // 1500):
    windlist.append(Wind(wind_0_1_x, wind_0_1_y, wind_0_1_width, wind_0_1_height, 0, player_1, 0, False))

wind_3_1_x = 150
wind_3_1_y = HEIGHT - 350
wind_3_1_width = 200
wind_3_1_height = 100
for _ in range((wind_3_1_width * wind_3_1_height) // 1500):
    windlist.append(Wind(wind_3_1_x, wind_3_1_y, wind_3_1_width, wind_3_1_height, 3, player_1, 0, True))

wind_3_2_x = 850
wind_3_2_y = HEIGHT - 700
wind_3_2_width = 150
wind_3_2_height = 100
for _ in range((wind_3_2_width * wind_3_2_height) // 1500):
    windlist.append(Wind(wind_3_2_x, wind_3_2_y, wind_3_2_width, wind_3_2_height, 3, player_1, 0, True))

wind_4_1_x = 150
wind_4_1_y = HEIGHT - 1000
wind_4_1_width = 250
wind_4_1_height = 300
for _ in range((wind_4_1_width * wind_4_1_height) // 3000):
    windlist.append(Wind(wind_4_1_x, wind_4_1_y, wind_4_1_width, wind_4_1_height, 4, player_1, 0, False))

wind_5_1_x = 900
wind_5_1_y = 250
wind_5_1_width = 250
wind_5_1_height = 100
for _ in range((wind_5_1_width * wind_5_1_height) // 1500):
    windlist.append(Wind(wind_5_1_x, wind_5_1_y, wind_5_1_width, wind_5_1_height, 5, player_1, 0, False))

wind_5_2_x = 1150
wind_5_2_y = HEIGHT - 350
wind_5_2_width = 250
wind_5_2_height = 200
for _ in range((wind_5_2_width * wind_5_2_height) // 1500):
    windlist.append(Wind(wind_5_2_x, wind_5_2_y, wind_5_2_width, wind_5_2_height, 5, player_1, 0, False))

wind_6_1_x = 450
wind_6_1_y = HEIGHT - 700
wind_6_1_width = 600
wind_6_1_height = 100
for _ in range((wind_6_1_width * wind_6_1_height) // 1500):
    windlist.append(Wind(wind_6_1_x, wind_6_1_y, wind_6_1_width, wind_6_1_height, 6, player_1, 0, False))

wind_7_1_x = 900
wind_7_1_y = 200
wind_7_1_width = 200
wind_7_1_height = 600
for _ in range((wind_7_1_width * wind_7_1_height) // 1500):
    windlist.append(Wind(wind_7_1_x, wind_7_1_y, wind_7_1_width, wind_7_1_height, 7, player_1, 0, False))

wind_8_1_x = 100
wind_8_1_y = 0
wind_8_1_width = WIDTH
wind_8_1_height = HEIGHT
for _ in range((wind_8_1_width * wind_8_1_height) // 1500):
    windlist.append(Wind(wind_8_1_x, wind_8_1_y, wind_8_1_width, wind_8_1_height, 8, player_1, 0, False))

#end create wind#####################################

#create Platform:####################################

platform_0_1 = Platform(0, HEIGHT - 150, 300, 150, False, 0, 0)
platform_0_2 = Platform(400, HEIGHT - 150, 150, 150, False, 0, 0)
platform_0_3 = Platform(550, HEIGHT - 450, 300, 450, False, 0, 0)
platform_0_4 = Platform(1100, HEIGHT - 350, 300, 350, False, 0, 0)
platform_0_5 = Platform(1400, HEIGHT - 500, WIDTH - 1400, 500, False, 0, 0)
platform_0_6 = Platform(0, 0, WIDTH, 5, False, 0, 0)
platform_0_7 = Platform(0, HEIGHT - 5, WIDTH, 5, False, 0, 0)

platform_1_1 = Platform(0, HEIGHT - 500, 400, 500, False, 1, 0)
platform_1_2 = Platform(550, 0, 150, HEIGHT - 250, False, 1, 0)
platform_1_3 = Platform(850, HEIGHT - 500, 200, 500, False, 1, 0)
platform_1_4 = Platform(1200, 0, 100, HEIGHT - 250, False, 1, 0)
platform_1_5 = Platform(1450, HEIGHT - 350, WIDTH - 1450, 350, False, 1, 0)
platform_1_6 = Platform(0, 0, WIDTH, 5, False, 1, 0)
platform_1_7 = Platform(0, HEIGHT - 5, WIDTH, 5, False, 1, 0)

platform_2_1 = Platform(0, 0, WIDTH, 5, False, 2, 0)
platform_2_2 = Platform(0, HEIGHT - 5, WIDTH, 5, False, 2, 0)

platform_3_1 = Platform(150, HEIGHT - 250, 200, 250, False, 3, 0)
platform_3_2 = Platform(550, HEIGHT - 200, 200, 200, False, 3, 0)
platform_3_3 = Platform(550, HEIGHT - 550, 150, 200, False, 3, 0)
platform_3_4 = Platform(850, HEIGHT - 600, 150, 600, False, 3, 0)
platform_3_5 = Platform(850, 0, 150, 250, False, 3, 0)
platform_3_6 = Platform(1200, HEIGHT - 700, 285, 700, False, 3, 0)
platform_3_7 = Platform(0, 0, WIDTH, 5, False, 3, 0)
platform_3_8 = Platform(0, HEIGHT - 5, WIDTH, 5, False, 3, 0)

platform_4_1 = Platform(0, HEIGHT - 700, 400, 700, False, 4, 0)
platform_4_2 = Platform(400, HEIGHT - 250, 300, 250, False, 4, 0)
platform_4_3 = Platform(700, HEIGHT - 450, 100, 450, False, 4, 0)
platform_4_4 = Platform(700, 0, 50, HEIGHT - 600, False, 4, 0)
platform_4_5 = Platform(1000, HEIGHT - 250, 300, 250, False, 4, 0)
platform_4_6 = Platform(1000, 100, 250, 500, True, 4, 250)
platform_4_7 = Platform(1250, 0, WIDTH - 1150, HEIGHT - 550, False, 4, 0)
platform_4_8 = Platform(0, 0, WIDTH, 5, False, 4, 0)
platform_4_9 = Platform(0, HEIGHT - 5, WIDTH, 5, False, 4, 0)

platform_5_1 = Platform(0, 0, 250, HEIGHT - 550, False, 5, 0)
platform_5_2 = Platform(300, HEIGHT - 150, WIDTH - 400, 150, False, 5, 0)
platform_5_3 = Platform(450, 350, 250, 400, True, 5, 100)
platform_5_4 = Platform(900, 350, 250, 350, False, 5, 0)
platform_5_5 = Platform(WIDTH - 100, HEIGHT - 450, 100, 450, False, 5, 0)
platform_5_6 = Platform(0, 0, WIDTH, 5, False, 5, 0)
platform_5_7 = Platform(0, HEIGHT - 5, WIDTH, 5, False, 5, 0)

platform_6_1 = Platform(0, HEIGHT - 450, 250, 450, False, 6, 0)
platform_6_2 = Platform(100, HEIGHT - 850, 50, 200, False, 6, 0)
platform_6_3 = Platform(250, HEIGHT - 850, 200, 200, False, 6, 0)
platform_6_4 = Platform(450, HEIGHT - 850, 300, 100, False, 6, 0)
platform_6_5 = Platform(250, HEIGHT - 150, 600, 150, False, 6, 0)
platform_6_6 = Platform(650, HEIGHT - 600, 400, 200, False, 6, 0)
platform_6_7 = Platform(1250, HEIGHT - 750, 150, 250, True, 6, 350)
platform_6_8 = Platform(WIDTH - 50, HEIGHT - 850, 50, 850, False, 6, 0)
platform_6_9 = Platform(0, 0, WIDTH, 5, False, 6, 0)
platform_6_10 = Platform(0, HEIGHT - 5, WIDTH, 5, False, 6, 0)

platform_7_1 = Platform(0, HEIGHT - 850, 100, 850, False, 7, 0)
platform_7_2 = Platform(250, HEIGHT - 400, 400, 400, False, 7, 0)
platform_7_3 = Platform(350, 0, 225, HEIGHT - 600, False, 7, 0)
platform_7_4 = Platform(900, 300, 200, 150, True, 7, 200)
platform_7_5 = Platform(1050, HEIGHT - 250, 200, 250, False, 7, 0)
platform_7_6 = Platform(1250, HEIGHT - 150, WIDTH - 1250, 150, False, 7, 0)
platform_7_7 = Platform(1250, 0, WIDTH - 1250, HEIGHT - 450, False, 7, 0)
platform_7_8 = Platform(0, 0, WIDTH, 5, False, 7, 0)
platform_7_9 = Platform(0, HEIGHT - 5, WIDTH, 5, False, 7, 0)

platform_8_1 = Platform(0, 0, 250, HEIGHT - 450, False, 8, 0)
platform_8_2 = Platform(0, HEIGHT - 150, WIDTH, 150, False, 8, 0)

#end create Platform:#################################

#background:#########################################
current_background = get_background_surface(config.current_backdrop)
settings_ui_elements = None
dragging_slider = False
#end background######################################

#background:#########################################
backgroundimage_nature = pygame.image.load("images/nature.jpg").convert()
backgroundimage_nature = pygame.transform.scale(backgroundimage_nature, (WIDTH, HEIGHT))
#end background######################################

player_1.change_character(config.current_character)

def ground():
    var_check_ground = vertical_bottom_y - 10
    player_bottom_y = vertical_bottom_y  # Current bottom position of player
    while True:
        if vertical_left_x > 0 and vertical_right_x < WIDTH and 0 < var_check_ground < HEIGHT:
                color_bottom_left = screen.get_at((horizontal_left_x, int(var_check_ground)))
                color_bottom_right = screen.get_at((horizontal_right_x, int(var_check_ground)))
                if (color_bottom_left[:3] in platformscolor) or (color_bottom_right[:3] in platformscolor):
                    detected_ground = var_check_ground - player_1.border
                    # The platform must be at or below the player's current bottom position
                    if var_check_ground >= player_bottom_y:
                        # NEVER update ground when jumping upward - prevents jump cancellation at any height
                        if player_1.state == "jump" and player_1.vel_y > 0:
                            # Don't update ground at all during upward jumps, regardless of wall contact
                            break
                        else:
                            # When falling or on ground, allow ground detection
                            if player_1.ground != detected_ground:
                                player_1.ground = detected_ground
                            break
                    else:
                        var_check_ground += 1
                else:
                    var_check_ground += 1
        elif (vertical_right_x >= WIDTH and 0 < var_check_ground < HEIGHT and WIDTH > horizontal_left_x > 0):
            color_bottom_left = screen.get_at((horizontal_left_x, int(var_check_ground)))
            if (color_bottom_left[:3] in platformscolor):
                    detected_ground = var_check_ground - player_1.border
                    if var_check_ground >= player_bottom_y:
                        # NEVER update ground when jumping upward - prevents jump cancellation
                        if player_1.state == "jump" and player_1.vel_y > 0:
                            break
                        player_1.ground = detected_ground
                        break
                    else:
                        var_check_ground += 1
            else:
                var_check_ground += 1
        
        elif vertical_left_x <= 0 and var_check_ground < HEIGHT:
            color_bottom_right = screen.get_at((horizontal_right_x, int(var_check_ground)))
            if (color_bottom_right[:3] in platformscolor):
                    detected_ground = var_check_ground - player_1.border
                    if var_check_ground >= player_bottom_y:
                        # NEVER update ground when jumping upward - prevents jump cancellation
                        if player_1.state == "jump" and player_1.vel_y > 0:
                            break
                        player_1.ground = detected_ground
                        break
                    else:
                        var_check_ground += 1
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
    while var_check_ceiling >= 0 and True:
        if vertical_left_x > 0 and vertical_right_x < WIDTH:
            check_y = max(0, int(var_check_ceiling))
            if check_y < HEIGHT:
                color_top_left = screen.get_at((vertical_left_x, check_y))
                color_top_right = screen.get_at((vertical_right_x, check_y))
                if (color_top_left[:3] in platformscolor) or (color_top_right[:3] in platformscolor):
                    player_1.ceiling = var_check_ceiling
                    break
            var_check_ceiling -= 1
        else:
            break

def check_bottom():
    if horizontal_left_x > 0 and horizontal_right_x < WIDTH and 0 < horizontal_bottom_y < HEIGHT:
        color_bottom_left = screen.get_at((horizontal_left_x, horizontal_bottom_y))
        color_bottom_right = screen.get_at((horizontal_right_x, horizontal_bottom_y))
        if (color_bottom_left[:3] not in platformscolor) and (color_bottom_right[:3] not in platformscolor): #fall down if not on ground
            check_fall(0)
        elif player_1.state != "jump":
            # Use consistent ground positioning
            player_1.y = player_1.ground - player_1.height - player_1.border

def check_fall(k):
    # Don't update ground when jumping upward (prevents jump cancellation)
    if not (player_1.state == "jump" and player_1.vel_y > 0):
        ground()
    if player_1.state != "jump":
        current_bottom = player_1.y + player_1.height + player_1.border
        if current_bottom < player_1.ground:
            player_1.vel_y += k * player_1.gravity  # Apply gravity
            player_1.y -= player_1.vel_y
            # Clamp immediately if we overshot the ground this frame
            new_bottom = player_1.y + player_1.height + player_1.border
            if new_bottom >= player_1.ground:
                player_1.y = player_1.ground - player_1.height - player_1.border
                player_1.vel_y = 0
        else:
            # Only adjust position if significantly off ground to prevent micro-adjustments
            target_y = player_1.ground - player_1.height - player_1.border
            if abs(player_1.y - target_y) > 0.5:  # Only adjust if more than 0.5 pixels off
                player_1.y = target_y
            player_1.vel_y = 0

def check_ceiling():
    if 0 < horizontal_right_x < WIDTH and 0 < horizontal_top_y < HEIGHT and 0 < horizontal_left_x < WIDTH:
            color_top_right = screen.get_at((horizontal_right_x, horizontal_top_y))
            color_top_left = screen.get_at((horizontal_left_x, horizontal_top_y))
            if color_top_right[:3] in platformscolor or color_top_left[:3] in platformscolor:
                ceiling()
                player_1.y = player_1.ceiling + player_1.border
                player_1.y += player_1.speed
                player_1.vel_y = 0  # Stop upward movement on collision 
    elif WIDTH >= horizontal_left_x > 0 and 0 < horizontal_top_y < HEIGHT:
            color_top_left = screen.get_at((horizontal_left_x, horizontal_top_y))
            if color_top_left[:3] in platformscolor:
                player_1.y += player_1.speed
                player_1.vel_y = 0  # Stop upward movement on collision
    elif horizontal_left_x <= 0 and WIDTH > horizontal_right_x > 0 and 0 < horizontal_top_y < HEIGHT:
            color_top_right = screen.get_at((horizontal_right_x, horizontal_top_y))
            if color_top_right[:3] in platformscolor:
                player_1.y += player_1.speed
                player_1.vel_y = 0  # Stop upward movement on collision

def check_left():
    if vertical_left_x > 0 and vertical_right_x <= WIDTH and vertical_bottom_y < HEIGHT and vertical_top_y > 0:
            color_left_top = screen.get_at((vertical_left_x, vertical_top_y + 5))
            color_left_bottom = screen.get_at((vertical_left_x, vertical_bottom_y - 5))
            if color_left_top[:3] in platformscolor or color_left_bottom[:3] in platformscolor:
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
            if color_right_top[:3] in platformscolor or color_right_bottom[:3] in platformscolor:
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

def resolve_ceiling_tunneling(prev_top_y, prev_left_x, prev_right_x):
    """
    Prevents the player from skipping through thin ceilings when moving upward
    with a large velocity in a single frame.
    """
    new_top_y = int(player_1.y - 1 - player_1.border)
    if new_top_y < prev_top_y:
        # Cover potential horizontal movement between frames
        left_x = max(0, min(prev_left_x, int(player_1.x)))
        right_x = min(WIDTH - 1, max(prev_right_x, int(player_1.x + player_1.width)))
        start_y = min(prev_top_y, HEIGHT - 1)
        end_y = max(new_top_y, -1)

        for y_scan in range(start_y, end_y - 1, -1):
            if y_scan < 0:
                # Clamp to the top of the screen if we overshoot past y = 0
                player_1.y = player_1.border + 1
                player_1.vel_y = 0
                break

            color_left = screen.get_at((left_x, y_scan))
            color_right = screen.get_at((right_x, y_scan))
            if color_left[:3] in platformscolor or color_right[:3] in platformscolor:
                # Place player just below the hit point
                player_1.y = y_scan + 1 + player_1.border
                player_1.vel_y = 0
                break


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


    img = Image.open(f"png_{player_1.character}/Run (1).png")   # no leading slash
    width, height = img.size
    
    # Initialize navigation bar elements (need to be available for event handling)
    pause = Antonio_font.render(pause_text, True, (0, 0, 0))
    pause_rect = pause.get_rect(topright=(WIDTH - 30, 0))
    restart = Antonio_font.render("RESTART", True, (0, 0, 0))
    restart_rect = restart.get_rect(topright=(WIDTH - pause_rect.width - 60, 0))
    settings = Antonio_font.render("SETTINGS", True, (0, 0, 0))
    settings_rect = settings.get_rect(topright=(WIDTH - pause_rect.width - restart_rect.width - 90, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: #start timer when any key is pressed
            if time_2 == 0:
                timer = True
                time_2 = pygame.time.get_ticks()
        if (player_1.command == True) and (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) and not player_1.state == "jump":
            player_1.jump()
            play_jump_sound(config.sound_volume, config.sound_enabled)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_1.settings_page:
                # Handle settings page clicks
                if settings_ui_elements:
                    result = handle_settings_click(event.pos, settings_ui_elements, player_1, platformscolor)
                    if result == "backdrop_changed":
                        # Update background when backdrop changes
                        current_background = get_background_surface(config.current_backdrop)
                        # Close settings and restart level with new backdrop
                        player_1.settings_page = False
                        reset_to_initial()
                    elif result == "character_changed":
                        # Close settings and restart level with new character
                        player_1.settings_page = False
                        reset_to_initial()
                    elif result == "back_clicked":
                        # Restart the level when back button is clicked (same as restart)
                        player_1.settings_page = False
                        reset_to_initial()
                    # Check if slider was clicked
                    if settings_ui_elements.get("slider_rect") and settings_ui_elements["slider_rect"].collidepoint(event.pos):
                        dragging_slider = True
            else:
                # Handle game UI clicks
                print("")

            if pause_rect.collidepoint(event.pos):
                    pause_function()
                    timer = False if pause_text == "RESUME" else True
            elif restart_rect.collidepoint(event.pos):
                    reset_to_initial()
            elif settings_rect.collidepoint(event.pos):
                    player_1.settings_page = True
                    pause_function()
        
        if event.type == pygame.MOUSEBUTTONUP:
            if player_1.settings_page:
                dragging_slider = False
        
        if event.type == pygame.MOUSEMOTION:
            if player_1.settings_page and dragging_slider and settings_ui_elements:
                handle_settings_drag(event.pos, settings_ui_elements)
                
            
    
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

        # Only allow gravity modification when jumping (prevents slow fall when not jumping)
        if player_1.state == "jump":
            if keys[pygame.K_DOWN]:
                player_1.gravity = -3
            elif keys[pygame.K_UP]:
                player_1.gravity = -0.5
            else:
                player_1.gravity = -1.5
        else:
            player_1.gravity = -1.5
        
        player_1.vel_x = 0
        player_1.collision_right = False
        player_1.collision_left = False
        
        #check left and right side of the person:
        if vertical_right_x < WIDTH and player_1.x > 0 and player_1.y > 0 and vertical_bottom_y < HEIGHT:
            color_right_top = screen.get_at((vertical_right_x , vertical_top_y + 5))
            color_right_bottom = screen.get_at((vertical_right_x, vertical_bottom_y - 5))
            if color_right_top[:3] in platformscolor or color_right_bottom[:3] in platformscolor:
                # Collision detected on right side
                player_1.collision_right = True
                if player_1.x + player_1.width > vertical_right_x:
                    # Player is inside the wall, push them back
                    player_1.x = vertical_right_x - player_1.width
                if player_1.wind_component > 0:
                    player_1.wind_component = 0
                if right:
                    player_1.vel_x = 0
                elif left:
                    player_1.vel_x = -player_1.speed
                # Wall jump mechanic (only if moving away from wall)
                if player_1.state == "jump" and left and player_1.vel_y > 0:
                    player_1.vel_y = 20
            elif right:
                player_1.vel_x = player_1.speed
        elif right:
            player_1.vel_x = player_1.speed


        if vertical_left_x > 0 and vertical_right_x <= WIDTH and vertical_bottom_y < HEIGHT and vertical_top_y > 0:
            color_left_top = screen.get_at((vertical_left_x, vertical_top_y + 5))
            color_left_bottom = screen.get_at((vertical_left_x, vertical_bottom_y - 5))
            if color_left_top[:3] in platformscolor or color_left_bottom[:3] in platformscolor:
                player_1.collision_left = True
                if player_1.x < vertical_left_x:
                    player_1.x = vertical_left_x
                if player_1.wind_component < 0:
                    player_1.wind_component = 0
                if left:
                    player_1.vel_x = 0
                elif right:
                    player_1.vel_x = player_1.speed
                # Wall jump mechanic (only if moving away from wall)
                if player_1.state == "jump" and right and player_1.vel_y > 0:
                    player_1.vel_y = 20
            elif left:
                player_1.vel_x = -player_1.speed
        elif left:
            player_1.vel_x = -player_1.speed
        
        #check top left and top right side of the person:
        # Only check ceiling when actually hitting the top of a platform, not when jumping toward walls
        if player_1.state == "jump" and player_1.vel_y > 0:
            # Don't check ceiling when touching walls - prevents false ceiling detection when jumping toward walls
            if not (player_1.collision_right or player_1.collision_left):
                check_y = max(0, horizontal_top_y)
                if 0 < horizontal_right_x < WIDTH and check_y < HEIGHT and 0 < horizontal_left_x < WIDTH:
                    color_top_right = screen.get_at((horizontal_right_x, check_y))
                    color_top_left = screen.get_at((horizontal_left_x, check_y))
                    if color_top_right[:3] in platformscolor or color_top_left[:3] in platformscolor:
                        ceiling()
                        player_1.y = player_1.ceiling + player_1.border
                        player_1.y += player_1.speed
                        player_1.vel_y = 0
                elif WIDTH >= horizontal_left_x > 0 and check_y < HEIGHT:
                    color_top_left = screen.get_at((horizontal_left_x, check_y))
                    if color_top_left[:3] in platformscolor:
                        player_1.y += player_1.speed
                        player_1.vel_y = 0
                elif horizontal_left_x <= 0 and WIDTH > horizontal_right_x > 0 and check_y < HEIGHT:
                    color_top_right = screen.get_at((horizontal_right_x, check_y))
                    if color_top_right[:3] in platformscolor:
                        player_1.y += player_1.speed
                        player_1.vel_y = 0
        # Only call check_fall when not jumping upward (prevents interference with jumps)
        if not (player_1.state == "jump" and player_1.vel_y > 0):
            check_fall(1)
      
        if player_1.state != "jump":
            #check bottom left and right side of the person:
            if horizontal_left_x > 0 and horizontal_right_x < WIDTH and 0 < horizontal_bottom_y < HEIGHT:
                color_bottom_left = screen.get_at((horizontal_left_x, horizontal_bottom_y))
                
                color_bottom_right = screen.get_at((horizontal_right_x, horizontal_bottom_y))
                if (color_bottom_left[:3] not in platformscolor) and (color_bottom_right[:3] not in platformscolor): #fall down if not on ground
                    check_fall(0)
                elif player_1.state != "jump":
                    player_1.y = player_1.ground - player_1.height - player_1.border
                    

        
        if timer == True:
            time_2 += 1
            candle.percentageheight -= 0.02
            candle.percentageheight = round(candle.percentageheight, 2)

        if timer == True and player_1.command == True:
            ghost_current.append((player_1.x, player_1.y, config.current_page, player_1.pngpath))
        
        
    player_1.update(horizontal_right_x)

    if player_1.command == True:
        if player_1.x + player_1.width > WIDTH:
            if config.current_page < config.max_pages:
                config.current_page += 1
                player_1.x = 0
                ground()
            else:
                # Reached the end of the last page - show success screen
                player_1.x = WIDTH - player_1.width
                player_1.success = True
        
        if player_1.x < 0:
            if config.current_page > 0:
                config.current_page -= 1
                player_1.x = WIDTH - player_1.width
                ground()
            else:
                player_1.x = 0

    # Recalculate positions after movement for collision checks
    post_move_left_x = int(player_1.x - player_1.border)
    post_move_right_x = int(player_1.x + player_1.width + player_1.border)
    post_move_top_y = int(player_1.y - player_1.border)
    post_move_bottom_y = int(player_1.y + player_1.height + player_1.border)
    
    # Check if player is inside a platform or too close to walls and push them out (prevents wall climbing)
    if player_1.command == True:
        # Check right side collision after movement
        if post_move_right_x < WIDTH and post_move_right_x > 0 and post_move_top_y > 0 and post_move_bottom_y < HEIGHT:
            check_right_x = post_move_right_x
            check_right_top = screen.get_at((check_right_x, post_move_top_y + 5))
            check_right_bottom = screen.get_at((check_right_x, post_move_bottom_y - 5))
            if check_right_top[:3] in platformscolor or check_right_bottom[:3] in platformscolor:
                # Player is touching or inside right wall, push them back
                player_1.x = check_right_x - 1 - player_1.width - player_1.border
                player_1.collision_right = True
                if player_1.wind_component > 0:
                    player_1.wind_component = 0
        
        # Check left side collision after movement
        if post_move_left_x > 0 and post_move_left_x < WIDTH and post_move_top_y > 0 and post_move_bottom_y < HEIGHT:
            check_left_x = post_move_left_x
            check_left_top = screen.get_at((check_left_x, post_move_top_y + 5))
            check_left_bottom = screen.get_at((check_left_x, post_move_bottom_y - 5))
            if check_left_top[:3] in platformscolor or check_left_bottom[:3] in platformscolor:
                # Player is touching or inside left wall, push them back
                player_1.x = check_left_x + 1 + player_1.border
                player_1.collision_left = True
                if player_1.wind_component < 0:
                    player_1.wind_component = 0
        
        # Check if player's center is inside a platform
        if not (player_1.state == "jump" and player_1.vel_y > 0):
            center_x = int(player_1.x + player_1.width / 2)
            center_y = int(player_1.y + player_1.height / 2)
            if 0 < center_x < WIDTH and 0 < center_y < HEIGHT:
                center_color = screen.get_at((center_x, center_y))
                if center_color[:3] in platformscolor:
                    # Player is inside a platform, push them out horizontally
                    test_x_left = int(player_1.x - player_1.speed - player_1.border)
                    test_x_right = int(player_1.x + player_1.width + player_1.speed + player_1.border)
                    pushed_out = False
                    
                    if test_x_left > 0:
                        test_color_left = screen.get_at((test_x_left, center_y))
                        if test_color_left[:3] not in platformscolor:
                            player_1.x -= player_1.speed
                            pushed_out = True
                    
                    # If left didn't work, try pushing right
                    if not pushed_out and test_x_right < WIDTH:
                        test_color_right = screen.get_at((test_x_right, center_y))
                        if test_color_right[:3] not in platformscolor:
                            player_1.x += player_1.speed
                            pushed_out = True
                    
                    # If still inside, try pushing up (but not during upward jumps)
                    if not pushed_out and player_1.state != "jump":
                        test_y_top = int(player_1.y - player_1.speed - player_1.border)
                        if test_y_top > 0:
                            test_color_top = screen.get_at((center_x, test_y_top))
                            if test_color_top[:3] not in platformscolor:
                                player_1.y -= player_1.speed

    # Checking if wind pushes player into a platform
    if player_1.command == True and player_1.wind_component != 0:
        # recalculate collision after wind
        check_right_x = int(player_1.x + player_1.width + 1 + player_1.border)
        check_left_x = int(player_1.x - 2 - player_1.border)
        check_top_y = int(player_1.y -player_1.border)
        check_bottom_y = int(player_1.y + player_1.height + player_1.border)

        #Check right side collision
        if check_right_x < WIDTH and player_1.x > 0 and player_1.y > 0 and check_bottom_y < HEIGHT:
            color_right_top = screen.get_at((check_right_x, check_top_y + 5))
            color_right_bottom = screen.get_at((check_right_x, check_bottom_y - 5))
            if (color_right_top[:3] in platformscolor or color_right_bottom[:3] in platformscolor) and player_1.wind_component > 0:
                player_1.x -= player_1.wind_component
                player_1.wind_component = 0

        if check_left_x > 0 and check_right_x <= WIDTH and check_bottom_y < HEIGHT:
            color_left_top = screen.get_at((check_left_x, check_top_y + 5))
            color_left_bottom = screen.get_at((check_left_x, check_bottom_y - 5))
            if (color_left_top[:3] in platformscolor or color_left_bottom[:3] in platformscolor) and player_1.wind_component < 0:
                player_1.x -= player_1.wind_component
                player_1.wind_component = 0

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
    
    final_wax_expanding = False
    for w in Wachs.instances:
        if hasattr(w, 'is_final') and w.is_final and hasattr(w, 'expanding') and w.expanding:
            final_wax_expanding = True
            break
    
    if player_1.success == False and player_1.fail == False or final_wax_expanding:
        widthbefore = player_1.width
        print("player pngpath:", player_1.pngpath)
        image = pygame.image.load(player_1.pngpath).convert_alpha()
        width = image.get_width()
        height = image.get_height()

        player_1.width = 100 * (width / height)
        if player_1.width > widthbefore:
            difference = player_1.width - widthbefore 
        if vertical_left_x - difference > 0 and vertical_bottom_y < HEIGHT and vertical_top_y > 0:
            color_left_top = screen.get_at((int(vertical_left_x - difference), vertical_top_y + 5))
            color_left_bottom = screen.get_at((int(vertical_left_x - difference), vertical_bottom_y - 5))
            if color_left_top[:3] in platformscolor or color_left_bottom[:3] in platformscolor:
                player_1.leftwall = True
            else:
                player_1.leftwall = False
        
        if player_1.leftwall == False:
            player_1.x = player_1.x - player_1.width + widthbefore
        
        screen.blit(current_background, (0, 0))

        if config.current_page == 0 and player_1.fail == False:
            
            move_text = Antonio_font.render("Use arrow keys to move left and right", True, (50, 255, 50))
            screen.blit(move_text, (50, HEIGHT - 500))
            
            jump_text1 = Antonio_font.render("Use [Space] to jump", True, (0, 0, 0))
            screen.blit(jump_text1, (450, HEIGHT - 700))
            jump_text2 = Antonio_font.render("Hold [Up] to jump higher", True, (0, 0, 0))
            screen.blit(jump_text2, (450, HEIGHT - 650))
            
            raindrop_warning = Antonio_font.render("Avoid the water!", True, (255, 0, 0))
            screen.blit(raindrop_warning, (300 + 75 - raindrop_warning.get_width() // 2, HEIGHT - 250))
            
            wind_warning = Antonio_font.render("Careful! Wind pushes you", True, (255, 0, 0))
            screen.blit(wind_warning, (1100, HEIGHT - 550))

        if config.current_page == 1 and player_1.fail == False:
            wax_text = Antonio_font.render("Collect the wax pieces to extend your timer", True, (255, 0, 0))
            screen.blit(wax_text, (50, 400))
            
            wall_jump_text = Antonio_font.render("You can jump against walls too", True, (255, 0, 0))
            screen.blit(wall_jump_text, (750, (HEIGHT // 2) - 100))

        # Page 2 - centered instructions with red wavy underlines
        if config.current_page == 2 and player_1.fail == False:
            # Text line 1: "Win by getting to the end before your"
            text1 = Antonio_font.render("Win by getting to the end before your", True, (0, 0, 0))
            text1_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
            screen.blit(text1, text1_rect)
            
            # Draw red wavy underline for text1
            start_x = text1_rect.left
            end_x = text1_rect.right
            y_pos = text1_rect.bottom + 5
            amplitude = 3
            frequency = 10
            for x in range(start_x, end_x, 2):
                wave_y = y_pos + int(amplitude * (x % (frequency * 2) - frequency) / frequency)
                pygame.draw.line(screen, (255, 0, 0), (x, wave_y), (min(x + 2, end_x), wave_y), 2)
            
            # Text line 2: "candle burns out!"
            text2 = Antonio_font.render("candle burns out!", True, (0, 0, 0))
            text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            screen.blit(text2, text2_rect)
            
            # Draw red wavy underline for text2
            start_x2 = text2_rect.left
            end_x2 = text2_rect.right
            y_pos2 = text2_rect.bottom + 5
            for x in range(start_x2, end_x2, 2):
                wave_y = y_pos2 + int(amplitude * (x % (frequency * 2) - frequency) / frequency)
                pygame.draw.line(screen, (255, 0, 0), (x, wave_y), (min(x + 2, end_x2), wave_y), 2)

        # draw ghost:
        if played_before == True:
            if timer == True:
                if len(ghost_best) > ghost_frame + 1:
                    ghost_frame += 1
                    ghost_x, ghost_y, ghost_current_page, ghost_pngpath = ghost_best[ghost_frame]
                    if ghost_current_page == config.current_page:                        

                        ghost_image = pygame.image.load(ghost_pngpath).convert_alpha()
                        ghost_image = pygame.transform.scale(
                            ghost_image, (player_1.width, player_1.height)
                        )

                        # convert image to grayscale
                        for x in range(ghost_image.get_width()):
                            for y in range(ghost_image.get_height()):
                                r, g, b, a = ghost_image.get_at((x, y))
                                gray = int(0.299*r + 0.587*g + 0.114*b)  # formel für grayscale
                                ghost_image.set_at((x, y), (gray, gray, gray, a))
                        
                        ghost_rect = pygame.Rect(ghost_x, ghost_y, player_1.width, player_1.height)   # position + siz
                        screen.blit(ghost_image, ghost_rect)
            elif ghost_frame != 0:
                ghost_rect = pygame.Rect(ghost_x, ghost_y, player_1.width, player_1.height)
                pygame.draw.rect(screen, (100,100,100), ghost_rect)

        draw = player_1.draw(screen)

        for raindrop in raindrops:
            draw = raindrop.draw(screen)
        
        for wind in windlist:
            draw = wind.draw(screen)
            config.check_wind = True

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

        # Check if final wax piece is still expanding
        final_wax_expanding = False
        for w in Wachs.instances:
            if w.is_final and w.expanding:
                final_wax_expanding = True
                # Continue drawing expansion animation
                w.draw(screen)
                text_y = HEIGHT // 2 - 100
                for dx in [-3, -2, -1, 0, 1, 2, 3]:
                    for dy in [-3, -2, -1, 0, 1, 2, 3]:
                        if dx != 0 or dy != 0:
                            outline = Antonio_font_big.render("YOU MADE IT!", True, (0, 0, 0))
                            outline_rect = outline.get_rect(center=(WIDTH // 2 + dx, text_y + dy))
                            screen.blit(outline, outline_rect)
                success = Antonio_font_big.render("YOU MADE IT!", True, (0, 255, 0))
                center_text = success.get_rect(center=(WIDTH // 2, text_y))
                screen.blit(success, center_text)
                break
        
        # Show text after expansion completes (if not already showing)
        if not final_wax_expanding:
            screen.fill((0, 0, 0))
            for dx in [-3, -2, -1, 0, 1, 2, 3]:
                for dy in [-3, -2, -1, 0, 1, 2, 3]:
                    if dx != 0 or dy != 0:
                        outline = Antonio_font_big.render("YOU MADE IT!", True, (0, 0, 0))
                        outline_rect = outline.get_rect(center=(WIDTH // 2 + dx, HEIGHT // 2 + dy))
                        screen.blit(outline, outline_rect)
            success = Antonio_font_big.render("YOU MADE IT!", True, (0, 255, 0))
            center_text = success.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(success, center_text)

    
    if player_1.settings_page == True:
        # Render settings page
        settings_ui_elements = render_settings(screen, Antonio_font, Antonio_font_big)
        # Ensure background and platform colors are up to date
        current_background = get_background_surface(config.current_backdrop)
        platformscolor[:] = get_platform_colors(config.current_backdrop)
    else:
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
