import pygame
from person import Person
from wachs import Wachs
from candle import Candle
from constants import *
import config
from PIL import Image

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

def draw_platform(surface, x, y, width, height):
    # 1. Create zig-zag top points
    color = [185, 145, 100]
    amplitude = 10
    step = 10
    points = []
    up = True
    for px in range(x, x + width + step, step):
        if up:
            points.append((px, y - amplitude + 20))
        else:
            points.append((px, y + 20))
        up = not up

    # 2. Add corners of the bottom rectangle to close the polygon
    points.append((x + width, y + height))  # bottom right corner
    points.append((x, y + height))          # bottom left corner

    # 3. Fill the polygon
    ghost_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (144, 187, 66), ghost_rect)

    pygame.draw.polygon(surface, color, points)
    

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # clear screen
    draw_platform(screen,x=100,y=200,width=790,height=100)

    pygame.display.flip()

pygame.quit()