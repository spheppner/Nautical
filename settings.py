# settings.py
# Centralized file for all game constants and configuration.

# Screen and Display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Nautical: LAN Edition"

# Networking
SERVER_HOST = "0.0.0.0" # Host on all available network interfaces
SERVER_PORT = 5555
MAX_PLAYERS = 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player Colors - Dictionary for programmatic access (e.g., UI, networking)
PLAYER_COLORS = {
    1: (50, 150, 255),   # Blue
    2: (255, 50, 50),    # Red
    3: (50, 255, 50),    # Green
    4: (255, 200, 50)    # Yellow
}


# UI Colors
BUTTON_COLOR = (30, 80, 150)
BUTTON_HOVER_COLOR = (50, 120, 200)
BUTTON_CLICK_COLOR = (10, 40, 100)

# World Generation
WORLD_WIDTH = 4000 # World dimension in pixels
WORLD_HEIGHT = 4000
TILE_SIZE = 10 # Visual size of a tile in pixels (for drawing)

# Calculated world dimensions in tiles
WORLD_TILES_X = WORLD_WIDTH // TILE_SIZE
WORLD_TILES_Y = WORLD_HEIGHT // TILE_SIZE

# Perlin Noise parameters for map generation
PERLIN_SCALE = 100.0
PERLIN_OCTAVES = 6
PERLIN_PERSISTENCE = 0.5
PERLIN_LACUNARITY = 2.0
WATER_LEVEL = 0.45 # Values below this are water
ISLAND_MIN_HEIGHT = 0.6

# Map Colors
WATER_COLOR = (20, 60, 120)
LAND_COLOR_LOW = (160, 140, 90)  # Sandy color for shores
LAND_COLOR_HIGH = (80, 120, 50)   # Grassy color for inland#
MOUTAIN_COLOR = (100, 100, 100)
FOG_COLOR = (30, 30, 40) # Dark blue/grey for Fog of War

# Game Logic and Ship Statistics
SHIP_STATS = {
    'command_center': {
        'speed': 0,
        'hp': 1000,
        'radar': 400,
        'image_size': (64, 64)
    },
    'cruiser': {
        'speed': 3,
        'hp': 250,
        'radar': 300,
        'image_size': (50, 25)
    },
    'scout': {
        'speed': 6,
        'hp': 75,
        'radar': 500,
        'image_size': (30, 15)
    }
}

# Combat Mechanics
MIN_SHOT_POWER = 200
MAX_SHOT_POWER = 1200
SHOT_CHARGE_RATE = 500  # Power per second
PROJECTILE_SPEED_MULTIPLIER = 1.0 # Multiplies shot power to get initial speed
PROJECTILE_GRAVITY = 200.0 # Pixels per second^2
PROJECTILE_DAMAGE = 100
EXPLOSION_RADIUS = 50 # Visual radius of the explosion effect
DESTRUCTION_RADIUS = 4 # Radius of terrain deformation in tiles

