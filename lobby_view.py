# lobby_view.py
import pygame
import socket
from settings import *
from ui import Button


class LobbyView:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.is_host = False
        self.lobby_state = None
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        self.start_game_button = Button(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Start Game")

    def on_enter(self, data):
        if data:
            self.is_host = data.get('is_host', False)

    def handle_event(self, event):
        if self.is_host:
            if self.start_game_button.handle_event(event):
                # Host clicks start, server sends start command
                start_command = {'type': 'start_game'}
                self.game_manager.network_server.broadcast_message(start_command)

    def update(self, dt):
        client = self.game_manager.network_client
        if client and client.last_message:
            msg = client.last_message
            if msg['type'] == 'lobby_update':
                self.lobby_state = msg['payload']
                client.last_message = None  # Consume the message
            elif msg['type'] == 'start_game':
                client.last_message = None
                self.game_manager.change_state("STRATEGY", {'lobby': self.lobby_state})

    def draw(self, screen):
        # Title
        title_surf = self.font.render("Game Lobby", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(title_surf, title_rect)

        # Display Host IP
        if self.is_host:
            try:
                # Get local IP to display
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
            except Exception:
                ip = "127.0.0.1"

            ip_surf = self.small_font.render(f"Your IP: {ip} - Share with friends!", True, GREEN)
            ip_rect = ip_surf.get_rect(center=(SCREEN_WIDTH / 2, 160))
            screen.blit(ip_surf, ip_rect)

        # Display connected players
        if self.lobby_state and 'players' in self.lobby_state:
            players = self.lobby_state['players']
            for i, player in enumerate(players):
                player_text = f"Player {player['id']}: {player['addr'][0]}"
                if player['id'] == self.game_manager.network_client.player_id:
                    player_text += " (You)"

                player_surf = self.font.render(player_text, True, WHITE)
                player_rect = player_surf.get_rect(center=(SCREEN_WIDTH / 2, 250 + i * 60))
                screen.blit(player_surf, player_rect)
        else:
            wait_text = "Waiting for players..." if self.is_host else "Connecting..."
            wait_surf = self.font.render(wait_text, True, WHITE)
            wait_rect = wait_surf.get_rect(center=(SCREEN_WIDTH / 2, 300))
            screen.blit(wait_surf, wait_rect)

        # Host specific UI
        if self.is_host:
            self.start_game_button.draw(screen)
        else:
            wait_surf = self.small_font.render("Waiting for host to start the game...", True, WHITE)
            wait_rect = wait_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100))
            screen.blit(wait_surf, wait_rect)
