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
        self.lobby_state = None

    def handle_event(self, event):
        if self.is_host and self.start_game_button.handle_event(event):
            print("Host clicked Start Game. Sending request to server...")
            self.game_manager.network_client.send_message({'type': 'start_game_request'})

    def update(self, dt):
        client = self.game_manager.network_client
        if client:
            # Process all messages in the queue
            for msg in client.get_messages():
                if msg['type'] == 'lobby_update':
                    self.lobby_state = msg['payload']
                elif msg['type'] == 'start_game':
                    print("Start game message received from server.")
                    self.game_manager.change_state("STRATEGY", {'initial_state': msg['payload']})
                    # Break because we are changing state
                    return

    def draw(self, screen):
        title_surf = self.font.render("Game Lobby", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(title_surf, title_rect)

        if self.is_host:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
            except Exception:
                ip = "127.0.0.1"
            ip_surf = self.small_font.render(f"Your IP: {ip} - Share with friends!", True, GREEN)
            ip_rect = ip_surf.get_rect(center=(SCREEN_WIDTH / 2, 160))
            screen.blit(ip_surf, ip_rect)

        client = self.game_manager.network_client
        if self.lobby_state and 'players' in self.lobby_state:
            players = self.lobby_state['players']
            for i, player in enumerate(players):
                player_text = f"Player {player['id']}: {player['addr'][0]}"
                if client and player['id'] == client.player_id:
                    player_text += " (You)"

                player_surf = self.font.render(player_text, True, WHITE)
                player_rect = player_surf.get_rect(center=(SCREEN_WIDTH / 2, 250 + i * 60))
                screen.blit(player_surf, player_rect)
        else:
            wait_text = "Waiting for players..." if self.is_host else "Connecting..."
            wait_surf = self.font.render(wait_text, True, WHITE)
            wait_rect = wait_surf.get_rect(center=(SCREEN_WIDTH / 2, 300))
            screen.blit(wait_surf, wait_rect)

        if self.is_host:
            self.start_game_button.draw(screen)
        else:
            wait_surf = self.small_font.render("Waiting for host to start the game...", True, WHITE)
            wait_rect = wait_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100))
            screen.blit(wait_surf, wait_rect)

