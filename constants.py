"""
Constants for Moses Adventure - Biblical Platformer Game
"""

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
LIGHT_GRAY = (200, 200, 200)

# Game physics
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5

# Game states
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    DIALOGUE = "dialogue"
    INVENTORY = "inventory"
    VICTORY = "victory"
    GAME_OVER = "game_over"

# Locations
class Location:
    PALACE = "palace"
    EGYPT_CITY = "egypt_city"
    DESERT = "desert"
    RED_SEA = "red_sea"
    WILDERNESS = "wilderness"
    MOUNT_SINAI = "mount_sinai"
    JERUSALEM = "jerusalem"
