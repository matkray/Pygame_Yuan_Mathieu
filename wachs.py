import pygame
from constants import *
import config

class Wachs:
    instances = []

    def __init__(self, x, y, page, player, candle, width=30, height=30, is_final=False):
        self.width = width
        self.height = height
        self.width_default = width
        self.height_default = height
        self.page = page
        self.x = x
        self.y = y
        self.show = True
        self.player_1 = player
        self.candle = candle
        self.is_final = is_final
        self.expanding = False
        self.expand_scale = 1.0
        self.expand_speed = 0.075
        Wachs.instances.append(self)
        

    def draw(self, screen):
        if self.expanding and self.page == config.current_page:
            self.expand_scale += self.expand_speed
            max_scale = max(WIDTH / self.width_default, HEIGHT / self.height_default) + 2.5
            if self.expand_scale >= max_scale:
                self.expand_scale = max_scale
                self.player_1.command = False
            
            if not hasattr(self, 'image') or self.image is None:
                self.image = pygame.image.load("images/wachsstueck.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width_default, self.height_default))
            
            expanded_width = int(self.width_default * self.expand_scale)
            expanded_height = int(self.height_default * self.expand_scale)
            expanded_x = WIDTH // 2 - expanded_width // 2
            expanded_y = HEIGHT // 2 - expanded_height // 2
            
            expanded_image = pygame.transform.scale(self.image, (expanded_width, expanded_height))
            screen.blit(expanded_image, (expanded_x, expanded_y))
            return
        
        if self.player_1.fail == False and self.page == config.current_page:
            self.rectwachs = pygame.Rect(self.x, self.y, self.width, self.height)
            
            if not hasattr(self, 'image') or self.image is None:
                self.image = pygame.image.load("images/wachsstueck.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            
            if self.show == True:
                if self.player_1.rectperson.colliderect(self.rectwachs):
                    if self.is_final:
                        self.expanding = True
                        self.show = False
                        self.player_1.success = True
                    else:
                        self.show = False
                        self.candle.percentageheight += 10
                else:
                    screen.blit(self.image, self.rectwachs)