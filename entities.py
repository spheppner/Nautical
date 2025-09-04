# entities.py
import pygame
from settings import *
from assets import assets


class BaseUnit(pygame.sprite.Sprite):
    """Base class for all units, now with proper sprites and network smoothing."""

    def __init__(self, pos, unit_type, player_owner, unique_id):
        super().__init__()
        self.unique_id = unique_id
        self.unit_type = unit_type
        self.stats = SHIP_STATS[unit_type]
        self.hp = self.stats['hp']
        self.max_hp = self.hp
        self.speed = self.stats['speed']
        self.radar_range = self.stats['radar_range']
        self.player_owner = player_owner

        self.image = assets.get_image(f'{unit_type}_{player_owner}')
        self.rect = self.image.get_rect(center=pos)

        # Network positions
        self.pos = pygame.math.Vector2(pos)  # This is the visual position
        self.server_pos = pygame.math.Vector2(pos)  # Authoritative position from server
        self.target_pos = pygame.math.Vector2(pos)  # Client-side move command

        self.selected = False

    def set_target(self, pos):
        self.target_pos = pygame.math.Vector2(pos)

    def update_from_state(self, state):
        """Updates the unit based on data from the server."""
        self.server_pos.x, self.server_pos.y = state['pos']
        self.hp = state['hp']

    def update(self):
        # Smoothly interpolate visual position towards server position
        self.pos = self.pos.lerp(self.server_pos, 0.2)  # Lerp for smoothness
        self.rect.center = self.pos

    def draw_extras(self, screen, camera):
        # Draw selection circle
        if self.selected:
            pygame.draw.circle(screen, WHITE, camera.apply(self.rect).center, self.rect.width, 1)
        # Draw movement line
        if self.pos.distance_to(self.target_pos) > 1:
            pygame.draw.line(screen, WHITE, camera.apply(self.rect).center, camera.apply_pos(self.target_pos), 1)

        # Draw HP bar
        if self.hp < self.max_hp:
            bar_rect = pygame.Rect(0, 0, self.rect.width, 5)
            bar_rect.midbottom = self.rect.midtop
            hp_ratio = self.hp / self.max_hp
            fill_rect = pygame.Rect(bar_rect.topleft, (bar_rect.width * hp_ratio, bar_rect.height))
            pygame.draw.rect(screen, RED, camera.apply(bar_rect))
            pygame.draw.rect(screen, GREEN, camera.apply(fill_rect))


class ArtilleryCruiser(BaseUnit):
    def __init__(self, pos, player_owner, unique_id):
        super().__init__(pos, 'cruiser', player_owner, unique_id)
        self.fire_range = self.stats['fire_range']


class ScoutShip(BaseUnit):
    def __init__(self, pos, player_owner, unique_id):
        super().__init__(pos, 'scout', player_owner, unique_id)


class CommandCenter(BaseUnit):
    def __init__(self, pos, player_owner, unique_id):
        super().__init__(pos, 'command_center', player_owner, unique_id)


def update(self):
    # Command center does not move, but we still need lerp for spawn-in
    self.pos = self.pos.lerp(self.server_pos, 0.2)
    self.rect.center = self.pos


# ... Projectile class remains largely the same ...
class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, velocity):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(velocity)
        self.image = pygame.Surface((6, 6))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, WHITE, (3, 3), 3)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.pos)
        self.age = 0

    def update(self, dt, world):
        self.velocity.y += PROJECTILE_GRAVITY * dt
        self.pos += self.velocity * dt
        self.rect.center = self.pos
        self.age += dt

        if not pygame.display.get_surface().get_rect().colliderect(self.rect) or self.age > 10:
            self.kill()

        if world.is_land(self.pos):
            world.deform_terrain(self.pos, DESTRUCTION_RADIUS)
            self.kill()

