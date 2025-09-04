# world.py
import pygame
import random
import math
from perlin import PerlinNoise  # <--- Changed from 'noise' library
from settings import *


class World:
    """
    Manages the generation of the world map from a seed.
    """

    def __init__(self, seed):
        self.seed = seed
        self.terrain_data = []
        self.perlin = PerlinNoise(octaves=4, seed=self.seed)  # <--- Instantiated our own class
        self.generate_terrain()
        self.map_surface = self.create_map_surface()
        self.valid_start_islands = self.find_valid_start_islands()

    def generate_terrain(self):
        """
        Creates a 2D array of height values using our internal Perlin noise generator and a radial gradient
        to form a central ocean with islands.
        """
        self.terrain_data = [[0 for _ in range(WORLD_TILES_X)] for _ in range(WORLD_TILES_Y)]
        center_x, center_y = WORLD_TILES_X / 2, WORLD_TILES_Y / 2

        for y in range(WORLD_TILES_Y):
            for x in range(WORLD_TILES_X):
                # Use our PerlinNoise class instance
                noise_val = self.perlin.noise(x * 0.05, y * 0.05)  # <--- Updated call

                # Radial gradient to create a central ocean
                dist_to_center = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                max_dist = math.sqrt(center_x ** 2 + center_y ** 2)
                gradient = dist_to_center / max_dist

                # Combine noise with the gradient
                height = (noise_val + (1.0 - gradient)) * 128 + 64

                self.terrain_data[y][x] = max(0, min(255, height))

    def find_valid_start_islands(self):
        """Finds reasonably large islands suitable for starting positions."""
        islands = []
        visited = set()
        for y in range(WORLD_TILES_Y):
            for x in range(WORLD_TILES_X):
                if (y, x) not in visited and self.terrain_data[y][x] > ISLAND_MIN_HEIGHT:
                    island_size = 0
                    center_x, center_y = 0, 0
                    stack = [(y, x)]
                    visited.add((y, x))

                    while stack:
                        cy, cx = stack.pop()
                        island_size += 1
                        center_x += cx
                        center_y += cy
                        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < WORLD_TILES_Y and 0 <= nx < WORLD_TILES_X and \
                                    (ny, nx) not in visited and self.terrain_data[ny][nx] > WATER_LEVEL:
                                visited.add((ny, nx))
                                stack.append((ny, nx))

                    if island_size > 20:  # Filter for decent sized islands
                        islands.append(((center_x // island_size) * TILE_SIZE, (center_y // island_size) * TILE_SIZE))

        random.shuffle(islands)
        return islands

    def get_tile_color(self, height):
        """Determine color based on height."""
        if height < WATER_LEVEL:
            return OCEAN_BLUE
        elif height < WATER_LEVEL + 15:
            return BEACH_YELLOW
        elif height < 180:
            return LAND_GREEN
        else:
            return MOUNTAIN_GREY

    def create_map_surface(self):
        """Renders the entire world terrain to a large pygame.Surface for efficiency."""
        world_surf = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        for y, row in enumerate(self.terrain_data):
            for x, height in enumerate(row):
                color = self.get_tile_color(height)
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(world_surf, color, rect)
        return world_surf

    def deform_terrain(self, world_pos, radius):
        """Modifies the terrain data and redraws the affected part of the map surface."""
        tile_x, tile_y = int(world_pos.x // TILE_SIZE), int(world_pos.y // TILE_SIZE)
        tile_radius = int(radius // TILE_SIZE)

        for y in range(max(0, tile_y - tile_radius), min(WORLD_TILES_Y, tile_y + tile_radius)):
            for x in range(max(0, tile_x - tile_radius), min(WORLD_TILES_X, tile_x + tile_radius)):
                dist_sq = (x - tile_x) ** 2 + (y - tile_y) ** 2
                if dist_sq < tile_radius ** 2:
                    new_height = self.terrain_data[y][x] - (tile_radius ** 2 - dist_sq) * 2
                    self.terrain_data[y][x] = max(0, new_height)
                    color = self.get_tile_color(self.terrain_data[y][x])
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.map_surface, color, rect)

    def get_height_at_pos(self, world_pos):
        """Returns the height value at a given world pixel position."""
        tile_x = int(world_pos.x // TILE_SIZE)
        tile_y = int(world_pos.y // TILE_SIZE)
        if 0 <= tile_x < WORLD_TILES_X and 0 <= tile_y < WORLD_TILES_Y:
            return self.terrain_data[tile_y][tile_x]
        return 0

    def is_land(self, world_pos):
        """Checks if a given pixel position is on land."""
        return self.get_height_at_pos(world_pos) >= WATER_LEVEL

