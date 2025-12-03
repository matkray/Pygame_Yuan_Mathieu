import pygame
from constants import *
import config

class Person:
    def __init__(self):
        self.speed = 3
        self.speed_default = self.speed
        self.width = 40
        self.height = 100

        self.x_default = 80
        self.x = self.x_default

        self.y_default = HEIGHT - self.height - 50
        self.y = self.y_default

        self.speed_x = 0
        self.gravity = -1.5
        self.ground = HEIGHT - self.height - 50
        self.vel_y = 0  # Vertical velocity for jumping
        self.vel_x = 0
        self.rectperson = pygame.Rect(self.x, self.y, self.width, self.height)
        self.command = True
        self.success = False
        self.ceiling = 0
        self.fail = False
        self.state = "jump" #or jump, dead, run, walk
        self.character = "dinosaurier" #or redhat
        self.maxrunframe = 8
        self.pngpath = f"Pygame_Yuan_Mathieu/png_{self.character}/Idle.png"
        self.jumpframe = 0
        self.walkframe = 0
        self.flipped = False
        self.start = True
        self.settings_page = False
        self.leftwall = False
        self.wind_component = 0
        self.border = 1
        self.collision_right = False
        self.collision_left = False

        
        
        
    def default(self):
        self.x = self.x_default
        self.y = self.y_default
        self.fail = False
        self.ground = HEIGHT
        self.flipped = False
        #self.jumpframe = 0
        self.walkframe = 0
        self.success = False
        self.command = True
        self.gravity = -1.5
        self.vel_x = 0
        self.vel_y = 0
        self.wind_component = 0
        

    def jump(self):
        if self.state != "jump":  # Only start jump if on ground
            self.state = "jump"
            self.vel_y = 20
    
    def change_character(self, character):
        self.character = character
        if character == "dinosaurier":
            self.maxrunframe = 10
        elif character == "santa":
            self.maxrunframe = 11
        elif character == "redhat":
            self.maxrunframe = 8
    
    def update(self, hallo):
        if self.command == True:
            before = self.y
            self.rectperson = pygame.Rect(self.x, self.y, self.width, self.height)
            if self.state == "jump":
                self.vel_y += self.gravity  # Apply gravity
                self.y -= self.vel_y  # Update position based on velocity

                if self.y + self.height >= self.ground:  # Stop falling at ground
                    self.y = self.ground - self.height
                    if self.vel_x == 0:
                        self.state = "idle"
                    else:
                        self.state = "walk"
                    self.vel_y = 0
    
            self.x += self.vel_x + self.wind_component
            self.border = self.wind_component + 1
            #print(self.wind_component if self.wind_component != 0 else "", self.border)
            


            if self.x >= WIDTH:
                self.x = -self.width + 1
                config.current_page += 1
                if config.current_page > config.max_pages:
                    self.command = False
                    self.success = True
                    self.vel_x = 0
                    self.vel_y = 0
            elif self.x + self.width < 0:
                self.x = WIDTH - 1
                config.current_page -= 1

            if self.state == "jump":
                self.walkframe = 0
                """self.jumpframe += 0.3
                self.jumpframe = self.jumpframe % 12
                if self.jumpframe >= 8:
                    self.jumpframe = 8"""
                self.pngpath = f"Pygame_Yuan_Mathieu/png_{self.character}/Jump.png"
            elif self.vel_x == 0:
                self.state == "idle"
                self.jumpframe = 0
                self.walkframe = 0
                self.pngpath = f"Pygame_Yuan_Mathieu/png_{self.character}/Idle.png"
            elif self.vel_y == 0:
                self.jumpframe = 0
                self.state == "walk"
                self.walkframe += 0.25
                self.walkframe = self.walkframe % (self.maxrunframe - 1)
                self.pngpath = f"Pygame_Yuan_Mathieu/png_{self.character}/Run ({round(self.walkframe) + 1}).png"


    def draw(self, screen):
        
        
        

        self.image = pygame.image.load(self.pngpath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        
        
        self.rectperson = pygame.Rect(self.x, self.y, self.width, self.height)   # position + siz
        if self.vel_x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = True
        elif self.vel_x > 0:
            self.flipped = False
        elif self.vel_x == 0 and self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        
        screen.blit(self.image, self.rectperson)

        #pygame.draw.rect(screen, (200,200,200), self.rectperson)