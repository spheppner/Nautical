# assets.py
# Centralized module for loading and creating game assets.
import pygame
from settings import *


class Assets:
    def __init__(self):
        self.images = {}
        self.generate_ship_images()

    def generate_ship_images(self):
        """Creates the surfaces for our ship sprites programmatically."""
        # Player 1 (Green Team)
        self.images['cruiser_1'] = self.create_ship_sprite(SHIP_STATS['cruiser']['image_size'], PLAYER_COLORS[1], PLAYER_COLORS[1])
        self.images['scout_1'] = self.create_ship_sprite(SHIP_STATS['scout']['image_size'], PLAYER_COLORS[1], PLAYER_COLORS[1], shape='triangle')
        self.images['command_center_1'] = self.create_ship_sprite(SHIP_STATS['command_center']['image_size'], PLAYER_COLORS[1], PLAYER_COLORS[1], shape='star')

        # Player 2 (Red Team)
        self.images['cruiser_2'] = self.create_ship_sprite(SHIP_STATS['cruiser']['image_size'], PLAYER_COLORS[2], PLAYER_COLORS[2])
        self.images['scout_2'] = self.create_ship_sprite(SHIP_STATS['scout']['image_size'], PLAYER_COLORS[2], PLAYER_COLORS[2], shape='triangle')
        self.images['command_center_2'] = self.create_ship_sprite(SHIP_STATS['command_center']['image_size'], PLAYER_COLORS[2], PLAYER_COLORS[2], shape='star')

        # Add more players if needed
        # Player 3 (Blue Team)
        self.images['cruiser_3'] = self.create_ship_sprite(SHIP_STATS['cruiser']['image_size'], PLAYER_COLORS[3], PLAYER_COLORS[3])
        self.images['scout_3'] = self.create_ship_sprite(SHIP_STATS['scout']['image_size'], PLAYER_COLORS[3], PLAYER_COLORS[3], shape='triangle')
        self.images['command_center_3'] = self.create_ship_sprite(SHIP_STATS['command_center']['image_size'], PLAYER_COLORS[3], PLAYER_COLORS[3], shape='star')

        # Player 4 (Yellow Team)
        self.images['cruiser_4'] = self.create_ship_sprite(SHIP_STATS['cruiser']['image_size'], PLAYER_COLORS[4], PLAYER_COLORS[4])
        self.images['scout_4'] = self.create_ship_sprite(SHIP_STATS['scout']['image_size'], PLAYER_COLORS[4], PLAYER_COLORS[4], shape='triangle')
        self.images['command_center_4'] = self.create_ship_sprite(SHIP_STATS['command_center']['image_size'], PLAYER_COLORS[4], PLAYER_COLORS[4], shape='star')

    def create_ship_sprite(self, size, color, dark_color, shape='rect'):
        """Creates a stylized ship surface."""
        w, h = size
        surf = pygame.Surface(size, pygame.SRCALPHA)

        if shape == 'rect':  # Cruiser
            pygame.draw.rect(surf, dark_color, (0, 0, w, h), border_radius=3)
            pygame.draw.rect(surf, color, (1, 1, w - 2, h - 2), border_radius=3)
            # Add a simple bridge
            pygame.draw.rect(surf, WHITE, (w * 0.6, h * 0.2, w * 0.3, h * 0.6))

        elif shape == 'triangle':  # Scout
            points = [(w / 2, 0), (0, h), (w, h)]
            pygame.draw.polygon(surf, dark_color, points)
            points_inner = [(w / 2, 2), (2, h - 2), (w - 2, h - 2)]
            pygame.draw.polygon(surf, color, points_inner)

        elif shape == 'star':  # Command Center
            points = []
            for i in range(10):
                angle = i * 36  # 360 / 10
                radius = w / 2 if i % 2 == 0 else w / 4
                x = w / 2 + radius * pygame.math.Vector2(1, 0).rotate(angle).x
                y = h / 2 + radius * pygame.math.Vector2(1, 0).rotate(angle).y
                points.append((x, y))
            pygame.draw.polygon(surf, dark_color, points)
            pygame.draw.polygon(surf, color, [(p[0], p[1]) for p in points], width=2)

        return surf

    def get_image(self, name):
        return self.images.get(name)


# Create a single instance to be imported by other modules
assets = Assets()
