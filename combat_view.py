# combat_view.py
import pygame
import math
from settings import *
from entities import Projectile


class CombatPlayer:
    """A controllable player in the combat view."""

    def __init__(self, pos, color, unit):
        self.pos = pygame.math.Vector2(pos)
        self.color = color
        self.unit = unit  # Reference to original unit
        self.rect = pygame.Rect(pos.x - 20, pos.y - 20, 40, 40)
        self.angle = 0
        self.power = 0
        self.is_charging = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw cannon
        end_x = self.rect.centerx + math.cos(self.angle) * 30
        end_y = self.rect.centery - math.sin(self.angle) * 30
        pygame.draw.line(screen, WHITE, self.rect.center, (end_x, end_y), 5)


class CombatView:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.projectiles = pygame.sprite.Group()
        self.combat_world = None
        self.attacker = None
        self.defender = None

    def on_enter(self, data):
        # Reset and setup combat
        self.projectiles.empty()
        self.combat_world = data['world_sector']

        # Position players on screen
        self.attacker = CombatPlayer(pygame.math.Vector2(100, SCREEN_HEIGHT - 100), GREEN, data['attacker'])
        self.defender = CombatPlayer(pygame.math.Vector2(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), RED, data['defender'])

        # For simplicity, create a flat ground for combat
        self.combat_terrain_slice = self.create_terrain_slice()

    def create_terrain_slice(self):
        """Creates a simplified 1D terrain slice for the combat view."""
        slice_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        slice_surf.fill((0, 0, 0, 0))
        # Draw a simple ground
        ground_y = SCREEN_HEIGHT - 50
        pygame.draw.rect(slice_surf, LAND_GREEN, (0, ground_y, SCREEN_WIDTH, 50))

        # Place players on the ground
        self.attacker.pos.y = ground_y - self.attacker.rect.height / 2
        self.attacker.rect.midbottom = (self.attacker.pos.x, ground_y)
        self.defender.pos.y = ground_y - self.defender.rect.height / 2
        self.defender.rect.midbottom = (self.defender.pos.x, ground_y)

        return slice_surf

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.attacker.is_charging = True
            if event.key == pygame.K_ESCAPE:  # End combat early
                self.end_combat()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and self.attacker.is_charging:
                self.fire_projectile(self.attacker)
                self.attacker.is_charging = False
                self.attacker.power = 0
                self.end_combat()  # For now, one shot ends combat

    def fire_projectile(self, player):
        start_pos = player.rect.center
        power = min(self.attacker.power, MAX_SHOT_POWER)
        velocity_x = math.cos(player.angle) * power
        velocity_y = -math.sin(player.angle) * power

        # Scale down velocity for gameplay
        vel = pygame.math.Vector2(velocity_x, velocity_y) * 0.5

        proj = Projectile(start_pos, vel)
        self.projectiles.add(proj)

    def end_combat(self):
        # In a real game, you would calculate damage here
        results = {"damage_dealt": random.randint(10, 50)}
        self.game_manager.change_state("STRATEGY", {"combat_results": results})

    def update(self, dt):
        # Aiming with mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.attacker.rect.centerx
        dy = mouse_y - self.attacker.rect.centery
        self.attacker.angle = math.atan2(-dy, dx)

        # Charging shot
        if self.attacker.is_charging:
            self.attacker.power += 500 * dt

        self.projectiles.update(dt, self.combat_world)  # Pass a dummy world for now

        # Check projectile collision with defender
        for proj in self.projectiles:
            if proj.rect.colliderect(self.defender.rect):
                print("HIT!")
                proj.kill()
                self.end_combat()

    def draw(self, screen):
        screen.fill(OCEAN_BLUE)
        screen.blit(self.combat_terrain_slice, (0, 0))
        self.attacker.draw(screen)
        self.defender.draw(screen)
        self.projectiles.draw(screen)

        # Draw power bar
        if self.attacker.is_charging:
            power_ratio = min(self.attacker.power / MAX_SHOT_POWER, 1.0)
            bar_width = 200
            fill_width = bar_width * power_ratio
            pygame.draw.rect(screen, RED, (10, 10, fill_width, 30))
            pygame.draw.rect(screen, WHITE, (10, 10, bar_width, 30), 2)
