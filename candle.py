import pygame
from constants import *
import random

#text stuff:########################################
pygame.font.init()
Antonio_font = pygame.font.Font('Antonio-Bold.ttf', 15)
#end text stuff:#####################################


class Candle:
    def __init__(self, player):
        self.maxheight = 100
        self.percentageheight = 100
        self.width = 30
        self.x = 60
        self.y = 120
        self.height_1 = (self.width / 42.34) *  42.539 
        self.height_1_default = self.height_1
        self.height_2 = (self.width / 42.34) * 7.627
        self.height_3 = (self.width / 42.34) * 6.949
        self.height_2_3 = (self.width / 42.34) * 14.569
        self.height_4 = (self.width / 42.34) * 85.140
        self.height_5 = (self.width / 42.34) * 4.775
        self.player_1 = player


        #1: 42.340 * 42.539
        #2: 42.340 * 7.627
        #3: 42.340 * 6.949
        #2-3: 42.340 * 14.569
        #4: 42.340 * 85.140
        #5: 42.340 * 4.775
        
    def draw(self, screen):
        if self.player_1.settings_page == False:
            if self.percentageheight > 100:
                self.percentageheight = 100
            if self.percentageheight < 0:
                self.percentageheight = 0

            self.height_1 = random.uniform(0.92, 1.08) * self.height_1
            if self.height_1 > 1.5 * self.height_1_default:
                self.height_1 = 1.5 * self.height_1_default
            elif self.height_1 < 0.5 * self.height_1_default:
                self.height_1 = 0.5 * self.height_1_default

            self.rectcandle1 = pygame.Rect(self.x, self.y - self.height_5 - self.percentageheight * 0.01 * self.height_4 - self.height_3 - self.height_2 - self.height_1 + 4, self.width, self.height_1)
            #self.rectcandle23 = pygame.Rect(self.x, self.y - self.height_5 - self.percentageheight * 0.01 * self.height_4 - self.height_2_3 + 4, self.width, self.height_2_3)
            self.rectcandle2 = pygame.Rect(self.x, self.y - self.height_5 - self.percentageheight * 0.01 * self.height_4 - self.height_3 - self.height_2 + 4, self.width, self.height_2)
            self.rectcandle3 = pygame.Rect(self.x, self.y - self.height_5 - self.percentageheight * 0.01 * self.height_4 - self.height_3 + 4, self.width, self.height_3)
            self.rectcandle4 = pygame.Rect(self.x, self.y - self.height_5 - self.percentageheight * 0.01 * self.height_4 + 2, self.width, self.percentageheight * 0.01 * self.height_4)
            self.rectcandle5 = pygame.Rect(self.x, self.y - self.height_5, self.width, self.height_5)

            self.candle_1 = pygame.image.load("candle/candle_1.png").convert_alpha()
            self.candle_1 = pygame.transform.scale(self.candle_1, (self.width, self.height_1))

            #self.candle_2_3 = pygame.image.load("candle/candle_2_3.png").convert_alpha()
            #self.candle_2_3 = pygame.transform.scale(self.candle_2_3, (self.width, self.height_2_3))

            if self.player_1.fail == False:
                self.candle_2 = pygame.image.load("candle/candle_2.png").convert_alpha()
            else:
                self.candle_2 = pygame.image.load("candle/candleblack_2.png").convert_alpha()
            self.candle_2 = pygame.transform.scale(self.candle_2, (self.width, self.height_2))

            self.candle_3 = pygame.image.load("candle/candle_3.png").convert_alpha()
            self.candle_3 = pygame.transform.scale(self.candle_3, (self.width, self.height_3))

            self.candle_4 = pygame.image.load("candle/candle_4.png").convert_alpha()
            if self.percentageheight > 0:
                self.candle_4 = pygame.transform.scale(self.candle_4, (self.width, self.percentageheight * 0.01 * self.height_4))
            else:
                self.player_1.fail == True
                self.candle_4 = pygame.transform.scale(self.candle_4, (self.width, self.percentageheight * 0.01 * self.height_4))

            self.candle_5 = pygame.image.load("candle/candle_5.png").convert_alpha()
            self.candle_5 = pygame.transform.scale(self.candle_5, (self.width, self.height_5))

            if self.percentageheight <= 10:            
                candle_percentage = Antonio_font.render(str(self.percentageheight)+"%", True, (255, 0, 0))
            else:
                candle_percentage = Antonio_font.render(str(self.percentageheight)+"%", True, (250, 250, 250))
            
            screen.blit(candle_percentage, (self.x, self.y))

            if self.percentageheight > 0:
                screen.blit(self.candle_1, self.rectcandle1)
            screen.blit(self.candle_2, self.rectcandle2)
            screen.blit(self.candle_3, self.rectcandle3)
            screen.blit(self.candle_4, self.rectcandle4)
            screen.blit(self.candle_5, self.rectcandle5)
        #elif self.player_1.fail == False
