# main_menu_view.py
import pygame
from settings import *
from ui import Button, TextInputBox


class MainMenuView:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.title_font = pygame.font.Font(None, 100)
        self.info_font = pygame.font.Font(None, 32)

        self.host_button = Button(SCREEN_WIDTH / 2 - 100, 300, 200, 50, "Host Game")
        self.join_button = Button(SCREEN_WIDTH / 2 - 100, 400, 200, 50, "Join Game")
        self.ip_input = TextInputBox(SCREEN_WIDTH / 2 - 150, 500, 300, 40)
        self.connect_button = Button(SCREEN_WIDTH / 2 - 100, 550, 200, 50, "Connect")

        self.show_join_ui = False
        self.error_message = ""

    def handle_event(self, event):
        if self.host_button.handle_event(event):
            self.game_manager.start_server()
            # Host also connects to their own server
            if self.game_manager.start_client('127.0.0.1'):
                self.game_manager.change_state("LOBBY", {'is_host': True})
            else:
                self.error_message = "Failed to start server."

        if self.join_button.handle_event(event):
            self.show_join_ui = True

        if self.show_join_ui:
            self.ip_input.handle_event(event)
            if self.connect_button.handle_event(event):
                ip_address = self.ip_input.text if self.ip_input.text else '127.0.0.1'
                if self.game_manager.start_client(ip_address):
                    self.game_manager.change_state("LOBBY", {'is_host': False})
                else:
                    self.error_message = f"Could not connect to {ip_address}"

    def update(self, dt):
        pass

    def draw(self, screen):
        # Title
        title_surf = self.title_font.render("Nautical", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, 150))
        screen.blit(title_surf, title_rect)

        # Buttons
        self.host_button.draw(screen)
        self.join_button.draw(screen)

        if self.show_join_ui:
            self.ip_input.draw(screen)
            self.connect_button.draw(screen)

            info_surf = self.info_font.render("Enter Host IP (leave blank for localhost):", True, WHITE)
            info_rect = info_surf.get_rect(center=(SCREEN_WIDTH / 2, 470))
            screen.blit(info_surf, info_rect)

        if self.error_message:
            error_surf = self.info_font.render(self.error_message, True, RED)
            error_rect = error_surf.get_rect(center=(SCREEN_WIDTH / 2, 650))
            screen.blit(error_surf, error_rect)

    def on_enter(self, data=None):
        self.show_join_ui = False
        self.error_message = ""
