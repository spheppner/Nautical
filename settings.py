# Centralized file for game constants.

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
OCEAN_BLUE = (20, 100, 180)
LAND_GREEN = (50, 150, 50)
BEACH_YELLOW = (220, 200, 100)
MOUNTAIN_GREY = (100, 100, 100)
FOG_COLOR = (50, 50, 60)

# Player Colors
P1_GREEN = (0, 220, 100)
P1_GREEN_DARK = (0, 100, 50)
P2_RED = (220, 50, 50)
P2_RED_DARK = (100, 20, 20)
P3_BLUE = (80, 150, 250)
P3_BLUE_DARK = (40, 75, 125)
P4_YELLOW = (250, 220, 50)
P4_YELLOW_DARK = (125, 110, 25)

# World Generation
TILE_SIZE = 16
WORLD_TILES_X = 150
WORLD_TILES_Y = 100
WORLD_WIDTH = WORLD_TILES_X * TILE_SIZE
WORLD_HEIGHT = WORLD_TILES_Y * TILE_SIZE
WATER_LEVEL = 90  # Increased water level for more sea
ISLAND_MIN_HEIGHT = 110 # Min height to be a valid starting island

# Ship Stats
SHIP_STATS = {
    'scout': {
        'hp': 50,
        'speed': 8,
        'radar_range': 200,
        'image_size': (20, 20)
    },
    'cruiser': {
        'hp': 150,
        'speed': 4,
        'radar_range': 120,
        'fire_range': 250,
        'image_size': (30, 30)
    },
    'command_center': {
        'hp': 500,
        'speed': 0,
        'radar_range': 180,
        'image_size': (50, 50)
    }
}

# Combat Phase Settings
COMBAT_TIMER = 60  # seconds
PROJECTILE_SPEED = 300
PROJECTILE_GRAVITY = 200
MAX_SHOT_POWER = 1000
DESTRUCTION_RADIUS = 30
