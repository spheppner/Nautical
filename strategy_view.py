# strategy_view.py
# ... existing Camera class code ...
import pygame
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

        # Limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - SCREEN_WIDTH), x)  # right
        y = max(-(self.height - SCREEN_HEIGHT), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)


class StrategyView:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.world = None
        self.camera = None
        self.all_sprites = pygame.sprite.Group()
        self.selected_unit = None
        self.end_turn_button = Button(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 70, 200, 50, "End Turn", self.resolve_turn)

    def setup_game(self, lobby_data):
        self.world = World()
        self.camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
        self.all_sprites.empty()

        # Define starting positions
        start_positions = [
            (200, 200),
            (WORLD_WIDTH - 200, WORLD_HEIGHT - 200),
            (200, WORLD_HEIGHT - 200),
            (WORLD_WIDTH - 200, 200)
        ]

        players = lobby_data['players']
        for i, player in enumerate(players):
            player_id = player['id']
            pos = start_positions[i % len(start_positions)]  # Cycle through start positions

            # Give each player one of each ship type for now
            cruiser = ArtilleryCruiser(pos, player_owner=player_id)
            scout_pos = (pos[0] + 50, pos[1] + 50)
            scout = ScoutShip(scout_pos, player_owner=player_id)
            self.all_sprites.add(cruiser, scout)

    def resolve_turn(self):
        print("Resolving turn...")
        for sprite in self.all_sprites:
            sprite.update(1.0, self.world)

    def on_enter(self, data=None):
        if data and 'lobby' in data:
            self.setup_game(data['lobby'])
        elif data and 'combat_results' in data:
            print(f"Combat results received: {data['combat_results']}")

    def handle_event(self, event):
        self.end_turn_button.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            world_pos = self.get_mouse_world_pos()
            if event.button == 1:  # Left click - selection
                self.selected_unit = None
                for sprite in self.all_sprites:
                    # Allow selecting only your own units
                    if sprite.player_owner == self.game_manager.network_client.player_id:
                        if sprite.rect.collidepoint(world_pos):
                            self.selected_unit = sprite
                            sprite.selected = True
                        else:
                            sprite.selected = False

            if event.button == 3:  # Right click - set target
                if self.selected_unit:
                    self.selected_unit.set_target(world_pos)

            if event.button == 2:  # Middle click - Initiate combat (for testing)
                if self.selected_unit:
                    for sprite in self.all_sprites:
                        if sprite.rect.collidepoint(world_pos) and sprite.player_owner != self.selected_unit.player_owner:
                            dist = self.selected_unit.pos.distance_to(sprite.pos)
                            if isinstance(self.selected_unit, ArtilleryCruiser) and dist < self.selected_unit.fire_range:
                                combat_data = {
                                    'attacker': self.selected_unit,
                                    'defender': sprite,
                                    'world_sector': self.world
                                }
                                self.game_manager.change_state("COMBAT", combat_data)
                                return  # Prevent further processing

    def update(self, dt):
        if not self.camera: return  # Don't update if game not set up
        keys = pygame.key.get_pressed()
        cam_speed = 500 * dt
        if keys[pygame.K_LEFT]: self.camera.camera.x += cam_speed
        if keys[pygame.K_RIGHT]: self.camera.camera.x -= cam_speed
        if keys[pygame.K_UP]: self.camera.camera.y += cam_speed
        if keys[pygame.K_DOWN]: self.camera.camera.y -= cam_speed

        self.camera.camera.x = max(-(WORLD_WIDTH - SCREEN_WIDTH), min(0, self.camera.camera.x))
        self.camera.camera.y = max(-(WORLD_HEIGHT - SCREEN_HEIGHT), min(0, self.camera.camera.y))

    def draw(self, screen):
        if not self.world:  # Don't draw if game not set up
            return
        screen.blit(self.world.map_surface, self.camera.camera.topleft)

        for sprite in self.all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite.rect))
            if sprite.player_owner == self.game_manager.network_client.player_id:
                sprite.draw_extras(screen, self.camera)

        self.end_turn_button.draw(screen)

    def get_mouse_world_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.camera:
            world_x = mouse_pos[0] - self.camera.camera.x
            world_y = mouse_pos[1] - self.camera.camera.y
            return (world_x, world_y)
        return mouse_pos

