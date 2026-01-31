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
  },
  "cloud": {
    "type": "image",
    "background": "Pygame_Yuan_Mathieu/images/background_cloud.png",
    "primary_color": (150, 150, 160),
    "secondary_color": (120, 120, 130)
  },
  "forest": {
    "type": "image",
    "background": "Pygame_Yuan_Mathieu/images/background_forest.png",
    "primary_color": (139, 115, 85),
    "secondary_color": (101, 135, 67)
  },
  "mountain": {
    "type": "image",
    "background": "Pygame_Yuan_Mathieu/images/background_mountain.png",
    "primary_color": (120, 100, 90),
    "secondary_color": (90, 80, 75)
  }
}

def get_platform_colors(theme_name):
  theme = BACKDROP_THEMES[theme_name]
  return [theme["primary_color"], theme["secondary_color"]]