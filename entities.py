import pygame
from settings import *
from assets import assets

class BaseUnit(pygame.sprite.Sprite):
    def __init__(self, pos, player_owner, unique_id, unit_type):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.server_pos = pygame.math.Vector2(pos)  # Authoritative position from server
        self.target_pos = pygame.math.Vector2(pos)
        self.player_owner = player_owner
        self.unique_id = unique_id
        self.unit_type = unit_type

        self.image = assets.images[str(self.unit_type) + "_" + str(self.player_owner+1)]
        self.rect = self.image.get_rect(center=self.pos)

        self.selected = False
        self.radar_range = SHIP_STATS[self.unit_type]['radar']
        self.speed = SHIP_STATS[self.unit_type]['speed']

    def update_from_state(self, unit_data):
        self.server_pos.x, self.server_pos.y = unit_data['pos']
        # We don't snap self.pos directly, we interpolate towards it in update()

    def update(self, dt):
        # Interpolate position smoothly towards the server's position
        lerp_factor = 0.25  # Adjust for smoother or tighter movement
        self.pos.x += (self.server_pos.x - self.pos.x) * lerp_factor
        self.pos.y += (self.server_pos.y - self.pos.y) * lerp_factor
        self.rect.center = self.pos

    def set_target(self, pos):
        self.target_pos.x, self.target_pos.y = pos

    def draw_extras(self, screen, camera):
        # Draw selection circle
        if self.selected:
            pygame.draw.circle(screen, WHITE, camera.apply_pos(self.pos), self.rect.width / 2 + 4, 2)

        # Draw target line
        if self.pos.distance_to(self.target_pos) > 1 and self.unit_type != 'command_center':
            pygame.draw.line(screen, PLAYER_COLORS[self.player_owner], camera.apply_pos(self.pos), camera.apply_pos(self.target_pos), 1)
            pygame.draw.circle(screen, PLAYER_COLORS[self.player_owner], camera.apply_pos(self.target_pos), 5)


class ArtilleryCruiser(BaseUnit):
    def __init__(self, pos, player_owner, unique_id):
        super().__init__(pos, player_owner, unique_id, 'cruiser')


class ScoutShip(BaseUnit):
    def __init__(self, pos, player_owner, unique_id):
        super().__init__(pos, player_owner, unique_id, 'scout')


class CommandCenter(BaseUnit):
    def __init__(self, pos, player_owner, unique_id):
        super().__init__(pos, player_owner, unique_id, 'command_center')


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

