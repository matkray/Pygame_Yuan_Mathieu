"""
Backdrop theme system for the game.
Define backdrop themes with colors and background images.
"""

BACKDROP_THEMES = {
  "nature": {
    "type": "image",
    "background": "Pygame_Yuan_Mathieu/images/nature.jpg",
    "primary_color": (185, 145, 100),
    "secondary_color": (144, 187, 66)
  }
}

def get_platform_colors(theme_name):
  theme = BACKDROP_THEMES[theme_name]
  return [theme["primary_color"], theme["secondary_color"]]