import pygame
from constants import *
import config
from PIL import Image
import random

class Wind():
    instances = []
    def __init__(self, rect_x, rect_y, rect_width, rect_height, page, player, number, right):
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.wind_width = 20
        self.page = page
        self.player_1 = player
        self.number = number
        self.right = right #True -> right, False -> left
        self.component = False
        if self.right == False:
            self.vel_x = -2
        else:
            self.vel_x = 2
        
        width, height = Image.open("Pygame_Yuan_Mathieu/images/wind_black.png").size
        self.wind_height = (self.wind_width / width) * height

        self.rect_total = pygame.Rect(self.rect_x, self.rect_y, self.rect_width, self.rect_height)

        collision = True
        while collision:
            collision = False

            self.wind_x = random.randint(self.rect_x, self.rect_x + self.rect_width - self.wind_width)
            self.wind_y = random.randint(self.rect_y, self.rect_y + self.rect_height)
            self.rect_wind = pygame.Rect(self.wind_x, self.wind_y, self.wind_width, self.wind_height)

            for wind in Wind.instances:
                if wind is not self and self.rect_wind.colliderect(wind.rect_wind):
                    collision = True
                    break   # restart with a new random position

           


        self.image = pygame.image.load("Pygame_Yuan_Mathieu/images/wind_black.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.wind_width, self.wind_height))
        if self.right == False:
            self.image = pygame.transform.flip(self.image, True, False)

        Wind.instances.append(self)

    def update(self):
        if config.current_page == self.page and self.player_1.fail == False:
            self.wind_x += self.vel_x
            if self.wind_x >= self.rect_x + self.rect_width:
                self.wind_x -= self.rect_width
            if self.wind_x < self.rect_x:
                self.wind_x += self.rect_width
            
            self.rect_wind = pygame.Rect(self.wind_x, self.wind_y, self.wind_width, self.wind_height)
            if config.check_wind:
                self.player_1.wind_component = 0
            if self.player_1.rectperson.colliderect(self.rect_total) and config.check_wind:
                    if self.right:
                        if self.player_1.collision_right:
                            self.player_1.wind_component = 0
                        else:
                            self.player_1.wind_component = 2
                            config.check_wind == False
                    else:
                        if self.player_1.collision_left:
                            self.player_1.wind_component = 0
                        else:
                            self.player_1.wind_component = -2
                            config.check_wind == False
     
    def draw(self, screen):
        if config.current_page == self.page and self.player_1.fail == False:
            screen.blit(self.image, self.rect_wind)
