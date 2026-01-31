"""
Settings page UI for the game.
Provides visual interface for character selection, backdrop themes, and sound controls.
"""

import pygame
from constants import *
import config
from themes import BACKDROP_THEMES, get_platform_colors

pygame.mixer.init()

pygame.mixer.music.load("Pygame_Yuan_Mathieu/song/platformer_background_music.mp3")

pygame.mixer.music.play(-1)



def render_settings(screen, font, font_big):
    """Render the settings page UI"""
    screen.fill((30, 30, 40))  # Dark background
    
    # Title
    title = font_big.render("SETTINGS", True, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title, title_rect)
    
    # Character Selection Section
    char_y = 180
    char_label = font.render("Character:", True, (255, 255, 255))
    screen.blit(char_label, (100, char_y))
    
    characters = ["redhat", "santa", "dinosaurier"]
    char_names_display = {"redhat": "Red Hat", "santa": "Santa", "dinosaurier": "Dinosaur"}
    char_buttons = []
    char_button_width = 200
    char_button_height = 250
    char_spacing = 250
    char_start_x = 100
    
    for i, char in enumerate(characters):
        x = char_start_x + i * char_spacing
        y = char_y + 50
        rect = pygame.Rect(x, y, char_button_width, char_button_height)
        char_buttons.append((rect, char))
        
        # Button background
        if config.current_character == char:
            color = (100, 150, 200)  # Selected: blue
        else:
            color = (60, 60, 70)  # Unselected: dark gray
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 3)
        
        # Character name
        name_text = font.render(char_names_display[char], True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(x + char_button_width // 2, y + char_button_height - 30))
        screen.blit(name_text, name_rect)
        
        # Character preview (load first idle frame)
        try:
            preview_path = f"Pygame_Yuan_Mathieu/png_{char}/Idle.png"
            preview_img = pygame.image.load(preview_path).convert_alpha()
            # Scale to fit in button
            scale_factor = min(char_button_width * 0.8 / preview_img.get_width(), 
                             (char_button_height - 50) / preview_img.get_height())
            new_width = int(preview_img.get_width() * scale_factor)
            new_height = int(preview_img.get_height() * scale_factor)
            preview_img = pygame.transform.scale(preview_img, (new_width, new_height))
            preview_rect = preview_img.get_rect(center=(x + char_button_width // 2, y + (char_button_height - 50) // 2))
            screen.blit(preview_img, preview_rect)
        except:
            pass
    
    # Backdrop Selection Section
    backdrop_y = 500
    backdrop_label = font.render("Backdrop:", True, (255, 255, 255))
    screen.blit(backdrop_label, (100, backdrop_y))
    
    backdrop_names = list(BACKDROP_THEMES.keys())
    backdrop_display_names = {
        "nature": "Nature",
        "cloud": "Cloud",
        "forest": "Forest",
        "mountain": "Mountain"
    }
    backdrop_buttons = []
    backdrop_button_width = 150
    backdrop_button_height = 100
    backdrop_spacing = 170
    backdrop_start_x = 100
    backdrop_per_row = 4
    
    for i, backdrop in enumerate(backdrop_names):
        row = i // backdrop_per_row
        col = i % backdrop_per_row
        x = backdrop_start_x + col * backdrop_spacing
        y = backdrop_y + 50 + row * (backdrop_button_height + 50)
        rect = pygame.Rect(x, y, backdrop_button_width, backdrop_button_height)
        backdrop_buttons.append((rect, backdrop))
        
        # Button background - use theme colors
        theme = BACKDROP_THEMES[backdrop]
        if config.current_backdrop == backdrop:
            # Selected: brighter colors
            bg_color = theme["primary_color"]
            border_color = (255, 255, 0)  # Yellow border for selected
        else:
            # Unselected: darker colors
            bg_color = tuple(min(255, c // 2) for c in theme["primary_color"])
            border_color = (100, 100, 100)  # Gray border for unselected
        
        pygame.draw.rect(screen, bg_color, rect)
        pygame.draw.rect(screen, border_color, rect, 3)
        
        # Backdrop name
        name_text = font.render(backdrop_display_names[backdrop], True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(x + backdrop_button_width // 2, y + backdrop_button_height // 2))
        screen.blit(name_text, name_rect)
    
    # Sound Volume Section (always show)
    sound_y = backdrop_y + 50 + (len(backdrop_names) // backdrop_per_row + (1 if len(backdrop_names) % backdrop_per_row else 0)) * (backdrop_button_height + 50)
    
    sound_label = font.render("Sound Volume:", True, (255, 255, 255))
    screen.blit(sound_label, (100, sound_y))
    
    slider_x = 400
    slider_y = sound_y
    slider_width = 400
    slider_height = 30
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    slider_handle_width = 20
    slider_handle_x = slider_x + int(config.sound_volume * slider_width) - slider_handle_width // 2
    
    # Draw slider track
    pygame.draw.rect(screen, (100, 100, 100), slider_rect)
    pygame.draw.rect(screen, (200, 200, 200), slider_rect, 2)
    
    # Draw slider handle
    handle_rect = pygame.Rect(slider_handle_x, slider_y, slider_handle_width, slider_height)
    pygame.draw.rect(screen, (255, 255, 255), handle_rect)
    pygame.draw.rect(screen, (0, 0, 0), handle_rect, 2)
    
    # Volume percentage text
    volume_text = font.render(f"{int(config.sound_volume * 100)}%", True, (255, 255, 255))
    screen.blit(volume_text, (slider_x + slider_width + 20, sound_y))
    
    # Sound enabled toggle
    toggle_y = sound_y + 60
    toggle_label = font.render("Sound Effects:", True, (255, 255, 255))
    screen.blit(toggle_label, (100, toggle_y))
    
    toggle_x = 400
    toggle_width = 60
    toggle_height = 30
    toggle_rect = pygame.Rect(toggle_x, toggle_y, toggle_width, toggle_height)
    
    pygame.mixer.music.set_volume(config.sound_volume)
    if config.sound_enabled:
        toggle_color = (100, 200, 100)  # Green when enabled
        toggle_text = "ON"
        pygame.mixer.music.unpause()
        

    else:
        toggle_color = (200, 100, 100)  # Red when disabled
        toggle_text = "OFF"
        pygame.mixer.music.pause()


    
    pygame.draw.rect(screen, toggle_color, toggle_rect)
    pygame.draw.rect(screen, (255, 255, 255), toggle_rect, 2)
    toggle_text_rendered = font.render(toggle_text, True, (255, 255, 255))
    toggle_text_rect = toggle_text_rendered.get_rect(center=(toggle_x + toggle_width // 2, toggle_y + toggle_height // 2))
    screen.blit(toggle_text_rendered, toggle_text_rect)
    
    # Back button
    back_y = sound_y + 150
    back_text = font.render("BACK", True, (255, 255, 255))
    back_rect = pygame.Rect(WIDTH // 2 - 100, back_y, 200, 50)
    pygame.draw.rect(screen, (150, 150, 150), back_rect)
    pygame.draw.rect(screen, (255, 255, 255), back_rect, 3)
    back_text_rect = back_text.get_rect(center=(WIDTH // 2, back_y + 25))
    screen.blit(back_text, back_text_rect)
    
    return {
        "char_buttons": char_buttons,
        "backdrop_buttons": backdrop_buttons,
        "slider_rect": slider_rect,
        "toggle_rect": toggle_rect,
        "back_rect": back_rect
    }

def handle_settings_click(pos, ui_elements, player, global_platformscolor):
    """Handle mouse clicks on settings UI elements"""
    mouse_x, mouse_y = pos
    
    # Check character buttons
    for rect, char in ui_elements["char_buttons"]:
        if rect.collidepoint(pos):
            if config.current_character != char:
                config.current_character = char
                player.change_character(char)
            return "character_changed"
    
    # Check backdrop buttons
    for rect, backdrop in ui_elements["backdrop_buttons"]:
        if rect.collidepoint(pos):
            if config.current_backdrop != backdrop:
                config.current_backdrop = backdrop
                # Update platform colors
                global_platformscolor[:] = get_platform_colors(backdrop)
            return "backdrop_changed"
    
    # Check slider
    if ui_elements.get("slider_rect") and ui_elements["slider_rect"].collidepoint(pos):
        relative_x = mouse_x - ui_elements["slider_rect"].left
        config.sound_volume = max(0.0, min(1.0, relative_x / ui_elements["slider_rect"].width))
        return "volume_changed"
    
    # Check toggle
    if ui_elements.get("toggle_rect") and ui_elements["toggle_rect"].collidepoint(pos):
        config.sound_enabled = not config.sound_enabled
        return "toggle_changed"
    
    # Check back button
    if ui_elements["back_rect"].collidepoint(pos):
        player.settings_page = False
        return "back_clicked"
    
    return None

def handle_settings_drag(pos, ui_elements):
    """Handle mouse dragging on slider"""
    if ui_elements.get("slider_rect") and ui_elements["slider_rect"].collidepoint(pos):
        mouse_x, mouse_y = pos
        relative_x = mouse_x - ui_elements["slider_rect"].left
        config.sound_volume = max(0.0, min(1.0, relative_x / ui_elements["slider_rect"].width))
        return True
    return False
