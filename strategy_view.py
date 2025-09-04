# strategy_view.py
import pygame
import math
from settings import *
from world import World
from entities import ArtilleryCruiser, ScoutShip, CommandCenter
from ui import Button


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity_rect):
        return entity_rect.move(self.camera.topleft)

    def apply_pos(self, pos):
        return pos + self.camera.topleft

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)


class StrategyView:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.world = None
        self.camera = None
        self.all_sprites = pygame.sprite.Group()
        self.sprite_map = {}  # Maps unit_id to sprite object for quick lookup
        self.selected_unit = None
        self.pending_commands = []
        self.submit_turn_button = Button(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 70, 200, 50, "Submit Turn", self.submit_turn)
        self.fog_surface = None

    def initialize_from_gamestate(self, initial_state):
        """Builds the game world and sprites from the server's initial state."""
        print("Initializing strategy view from server state...")
        self.world = World(seed=initial_state['world_seed'])
        self.camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
        self.all_sprites.empty()
        self.sprite_map.clear()

        self.fog_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.fog_surface.fill(FOG_COLOR)
        self.fog_surface.set_colorkey((255, 0, 255))  # Make a color transparent

        for unit_id, unit_data in initial_state['units'].items():
            pos = unit_data['pos']
            unit_type = unit_data['type']
            player_owner = unit_data['owner']

            sprite = None
            if unit_type == 'cruiser':
                sprite = ArtilleryCruiser(pos, player_owner, unit_id)
            elif unit_type == 'scout':
                sprite = ScoutShip(pos, player_owner, unit_id)
            elif unit_type == 'command_center':
                sprite = CommandCenter(pos, player_owner, unit_id)

            if sprite:
                self.all_sprites.add(sprite)
                self.sprite_map[unit_id] = sprite
        print(f"Created {len(self.all_sprites)} sprites.")

    def submit_turn(self):
        if self.pending_commands:
            print(f"Submitting {len(self.pending_commands)} commands to server...")
            self.game_manager.network_client.send_commands(self.pending_commands)
            self.pending_commands = []
        else:
            print("No commands to submit.")

    def on_enter(self, data=None):
        if data and 'initial_state' in data:
            self.initialize_from_gamestate(data['initial_state'])
        elif data and 'combat_results' in data:
            print(f"Combat results received: {data['combat_results']}")

    def handle_event(self, event):
        if not self.world: return
        self.submit_turn_button.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            world_pos = self.get_mouse_world_pos()
            if event.button == 1:  # Left click
                self.selected_unit = None
                for sprite in self.all_sprites:
                    sprite.selected = False
                    if sprite.player_owner == self.game_manager.network_client.player_id:
                        if sprite.rect.collidepoint(world_pos):
                            self.selected_unit = sprite
                            sprite.selected = True

            if event.button == 3:  # Right click
                if self.selected_unit and not self.world.is_land(pygame.math.Vector2(world_pos)):
                    self.selected_unit.set_target(world_pos)
                    self.pending_commands = [c for c in self.pending_commands if c['unit_id'] != self.selected_unit.unique_id]
                    command = {
                        'action': 'move',
                        'unit_id': self.selected_unit.unique_id,
                        'target': world_pos
                    }
                    self.pending_commands.append(command)

    def update(self, dt):
        if not self.camera: return
        client = self.game_manager.network_client
        if client:
            for msg in client.get_messages():
                if msg['type'] == 'game_update':
                    game_state = msg['payload']
                    for unit_id, unit_data in game_state['units'].items():
                        if unit_id in self.sprite_map:
                            self.sprite_map[unit_id].update_from_state(unit_data)

        self.all_sprites.update(dt)  # Pass delta time for smooth movement

        keys = pygame.key.get_pressed()
        cam_speed = 500 * dt
        if keys[pygame.K_LEFT]: self.camera.camera.x += cam_speed
        if keys[pygame.K_RIGHT]: self.camera.camera.x -= cam_speed
        if keys[pygame.K_UP]: self.camera.camera.y += cam_speed
        if keys[pygame.K_DOWN]: self.camera.camera.y -= cam_speed
        self.camera.camera.x = max(-(WORLD_WIDTH - SCREEN_WIDTH), min(0, self.camera.camera.x))
        self.camera.camera.y = max(-(WORLD_HEIGHT - SCREEN_HEIGHT), min(0, self.camera.camera.y))

    def draw(self, screen):
        if not self.world: return
        screen.blit(self.world.map_surface, self.camera.camera.topleft)

        my_player_id = self.game_manager.network_client.player_id
        my_units = [s for s in self.all_sprites if s.player_owner == my_player_id]

        visible_sprites = set(my_units)
        for unit in self.all_sprites:
            if unit.player_owner != my_player_id:
                for my_unit in my_units:
                    if unit.pos.distance_to(my_unit.pos) <= my_unit.radar_range:
                        visible_sprites.add(unit)
                        break

        for sprite in self.all_sprites:
            if sprite in visible_sprites:
                screen.blit(sprite.image, self.camera.apply(sprite.rect))
                sprite.draw_extras(screen, self.camera)

        if self.fog_surface:
            self.fog_surface.fill(FOG_COLOR)
            self.fog_surface.blit(self.world.map_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            for my_unit in my_units:
                pygame.draw.circle(self.fog_surface, (255, 0, 255), my_unit.pos, my_unit.radar_range)
            screen.blit(self.fog_surface, self.camera.camera.topleft)

        self.submit_turn_button.draw(screen)

    def get_mouse_world_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.camera:
            world_x = mouse_pos[0] - self.camera.camera.x
            world_y = mouse_pos[1] - self.camera.camera.y
            return (world_x, world_y)
        return mouse_pos

