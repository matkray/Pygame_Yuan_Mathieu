import pygame
from constants import *
import config
from PIL import Image
import random
from themes import get_platform_colors

class Platform:
    instances = []
    def __init__(self, x, y, width, height, move, page, y_difference):
        self.x = x
        self.y = y
        self.y_difference = y_difference
        self.width = width
        self.height = height
        self.move = move
        if self.move == True:
            self.v_y = 1
            self.v_y_default = self.v_y
        else:
            self.v_y = 0
            self.v_y_default = self.v_y
        self.page = page

        self.y_default = self.y

        if self.y_difference > 0:
            self.y_upper_limit = self.y
            self.y_lower_limit = self.y + self.y_difference
        else:
            self.y_upper_limit = self.y + self.y_difference
            self.y_lower_limit = self.y

        self.instances.append(self)

        if page > config.max_pages:
            config.max_pages = page


    def update(self):
        if self.move == True:
            if self.y > self.y_lower_limit or self.y < self.y_upper_limit:
                self.v_y = -self.v_y
                self.v_y_default = self.v_y
            
            self.y += self.v_y
    def draw(self, screen):
        if self.page == config.current_page:
            colors = get_platform_colors(config.current_backdrop)
            green = colors[0]
            brown = colors[1]

            amplitude = 10
            step = 10
            points = []
            up = True
            for px in range(int(self.x), int(self.x + self.width) + step, step):
                if up:
                    points.append((px, self.y - amplitude + 20))
                else:
                    points.append((px, self.y + 20))
                up = not up

            points.append((self.x + self.width, self.y + self.height))
            points.append((self.x, self.y + self.height))

            green_rect = pygame.Rect(self.x, self.y, self.width + 1, self.height) #green rectangle
            pygame.draw.rect(screen, brown, green_rect) #brown rectangle with 

            pygame.draw.polygon(screen, green, points) #brown rectangle with zigzag