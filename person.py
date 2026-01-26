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

        self.y_default = HEIGHT - 100 - self.height
        self.y = self.y_default

        self.speed_x = 0
        self.gravity = -1.5
        self.ground = HEIGHT - 100
        self.vel_y = 0  # Vertical velocity for jumping
        self.vel_x = 0
        self.rectperson = pygame.Rect(self.x, self.y, self.width, self.height)
        self.command = True
        self.success = False
        self.ceiling = 0
        self.fail = False
        self.state = "idle" #or jump, dead, run, walk, idle
        self.character = "dinosaurier" #or redhat etc
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
        self.side_collision_wind_push = False
        self.locked_y_position = 0
        self.has_side_collision = False
        self.just_jumped = False
        self.jump_start_ground = HEIGHT - 100  # Store ground value at jump start

        
        
        
    def default(self):
        self.x = self.x_default
        self.y = self.y_default
        self.fail = False
        self.ground = HEIGHT - 100
        self.flipped = False
        #self.jumpframe = 0
        self.walkframe = 0
        self.success = False
        self.command = True
        self.gravity = -1.5
        self.vel_x = 0
        self.vel_y = 0
        self.wind_component = 0
        self.state = "idle"
        self.side_collision_wind_push = False
        self.has_side_collision = False
        self.collision_right = False
        self.collision_left = False
        self.just_jumped = False
        self.border = 1
        self.jump_start_ground = HEIGHT - 100
        self.start = True
        

    def jump(self):
        if self.vel_y <= 15:
            self.state = "jump"
            self.vel_y = 20
            self.side_collision_wind_push = False
            self.has_side_collision = False
            # Store the ground value at jump start to prevent interference during jump
            self.jump_start_ground = self.ground
    
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
                current_bottom = self.y + self.height
                # When jumping upward, completely ignore ground checks to reach maximum height
                if self.vel_y > 0:
                    self.vel_y += self.gravity
                    self.y -= self.vel_y
                elif self.vel_y <= 0:
                    # Only check ground when falling or at rest
                    if current_bottom < self.ground:
                        # Still falling, continue falling
                        self.vel_y += self.gravity
                        self.y -= self.vel_y
                    else:
                        # Landed on ground
                        was_jumping = self.state == "jump"
                        self.y = self.ground - self.height - self.border
                        self.vel_y = 0
                        new_state = "idle" if self.vel_x == 0 else "walk"
                        # Play landing sound if we just landed
                        if was_jumping and new_state != "jump":
                            from sound_manager import play_landing_sound
                            play_landing_sound(config.sound_volume, config.sound_enabled)
                        self.state = new_state
            else:
                # Don't reset vel_y when falling - let check_fall() handle velocity accumulation
                # Only reset if we're actually on the ground (check_fall will set it to 0 when on ground)
                current_bottom = self.y + self.height + self.border
                if current_bottom >= self.ground:
                    # On ground, reset velocity
                    self.vel_y = 0
                # If falling (current_bottom < self.ground), keep vel_y so it can accumulate in check_fall()
    
            # Prevent wind from pushing into walls
            wind_x = self.wind_component
            if self.collision_right and wind_x > 0:
                wind_x = 0
            if self.collision_left and wind_x < 0:
                wind_x = 0
            
            self.x += self.vel_x + wind_x
            # Only stabilize border when against walls and NOT jumping (prevents interference with jump physics)
            if (self.collision_right or self.collision_left) and self.state != "jump":
                # Keep border at minimum when against walls to prevent position changes
                self.border = 1
            else:
                self.border = abs(self.wind_component) + 1
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
                self.state = "idle"
                self.jumpframe = 0
                self.walkframe = 0
                self.pngpath = f"Pygame_Yuan_Mathieu/png_{self.character}/Idle.png"
            else:
                self.jumpframe = 0
                self.state = "walk"
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