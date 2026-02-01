import pygame
from constants import *
import config

class Wachs:
    instances = []

    def __init__(self, x, y, page, player, candle):
        self.width = 30
        self.height = 30
        self.page = page
        self.x = x
        self.y = y
        self.show = True
        self.player_1 = player
        self.candle = candle
        Wachs.instances.append(self)
        

    def draw(self, screen):
        if self.player_1.fail == False:
            #if self.page == config.current_page:
            self.rectwachs = pygame.Rect(self.x, self.y, self.width, self.height)   # position + siz

            self.image = pygame.image.load("images/wachsstueck.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

            
            if self.show == True:
                if self.player_1.rectperson.colliderect(self.rectwachs) or self.page != config.current_page:
                    self.show = False
                    self.candle.percentageheight += 10
                elif self.show == True:
                    screen.blit(self.image, self.rectwachs)