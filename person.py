# Example file showing a basic pygame "game loop"
import pygame
import math
import random
from constants import *
from time import sleep
import config





class Person:
    def __init__(self):
        self.speed = 2
        self.width = 40
        self.height = 100
        self.x = 50
        self.y = HEIGHT - self.height - 50
        self.speed_x = 0
        self.gravity = -1.5
        self.ground = HEIGHT - self.height - 50
        self.is_jumping = False
        self.vel_y = 0  # Vertical velocity for jumping
        self.vel_x = 0
        self.candle_percentage = 100
        self.rectperson = pygame.Rect(self.x, self.y, self.width, self.height)
        self.command = True
        self.success = False

    def jump(self):
        if not self.is_jumping:  # Only start jump if on ground
            self.is_jumping = True
            self.vel_y = 20
    
    def update(self):
        self.rectperson = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.is_jumping:
            self.vel_y += self.gravity  # Apply gravity
            self.y -= self.vel_y  # Update position based on velocity

            if self.y + self.height >= self.ground:  # Stop falling at ground
                self.y = self.ground - self.height
                self.is_jumping = False
                self.vel_y = 0
        
        
        self.x += self.vel_x


        #elif self.x + self.width + 5 > WIDTH:
        #    self.x = WIDTH - self.width - 20
        
        if self.x > WIDTH:
            self.x = 0
            config.current_page += 1
            if config.current_page > len(config.platforms) - 1:
                self.command = False
                self.success = True
                self.vel_x = 0
                self.vel_y = 0
        elif self.x + self.width < 0:
            self.x = WIDTH - self.width
            config.current_page -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, (200,200,200), self.rectperson)

    #def update(self):
    #    self.y -= self.vy
