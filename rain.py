import pygame
from constants import *
import config
from PIL import Image
import random


"""class Rainrectangle:
    def __init__(self, x, y, width, height, page, player):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.page = page
        self.player_1 = player"""

    #def draw(self):

class Raindrop():
    instances = []
    def __init__(self, rect_x, rect_y, rect_width, rect_height, page, player, candle, number):
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.drop_width = 10
        self.page = page
        self.player_1 = player
        self.candle = candle
        self.gravitation = 4
        self.number = number
        
        width, height = Image.open("Pygame_Yuan_Mathieu/images/raindrop.png").size
        self.drop_height = (self.drop_width / width) * height


        collision = True
        while collision:
            collision = False

            self.raindrop_x = random.randint(self.rect_x, self.rect_x + self.rect_width - self.drop_width)
            self.raindrop_y = random.randint(self.rect_y, self.rect_y + self.rect_height)
            self.rect_rain = pygame.Rect(self.raindrop_x, self.raindrop_y, self.drop_width, self.drop_height)

            for raindrop in Raindrop.instances:
                if raindrop is not self and self.rect_rain.colliderect(raindrop.rect_rain):
                    collision = True
                    break   # restart with a new random position


        self.image = pygame.image.load("Pygame_Yuan_Mathieu/images/raindrop.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.drop_width, self.drop_height))

        Raindrop.instances.append(self)

    def update(self):
        if config.current_page == self.page and self.player_1.fail == False:
            self.raindrop_y += self.gravitation
            if self.raindrop_y >= self.rect_y + self.rect_height:
                self.raindrop_y -= self.rect_height
            
            self.rect_rain = pygame.Rect(self.raindrop_x, self.raindrop_y, self.drop_width, self.drop_height)

            if self.player_1.rectperson.colliderect(self.rect_rain):
                self.candle.percentageheight -= 1
     
    def draw(self, screen):
        if config.current_page == self.page and self.player_1.fail == False:
            screen.blit(self.image, self.rect_rain)

            """if Raindrop.instances[self.number] == False:
                Raindrop.instances[self.number] = True
                whole_rect = pygame.Rect(self.rect_x, self.rect_y, self.rect_width, self.rect_height + self.drop_height)
                pygame.draw.rect(screen, (131,202,221), whole_rect, 2)"""

            """if self.show == True:
                if self.player_1.rectperson.colliderect(self.rectwachs) or self.page != config.current_page:
                    self.show = False
                    self.candle.percentageheight += 10
                elif self.show == True:
                    screen.blit(self.image, self.rectwachs)"""