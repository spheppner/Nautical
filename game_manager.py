import pygame
from settings import *

from main_menu_view import MainMenuView
from lobby_view import LobbyView
from strategy_view import StrategyView
from combat_view import CombatView
from networking import NetworkServer, NetworkClient


class Game:
    """
    Manages the main game loop and transitions between game states.
    """

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # Networking instances
        self.network_server = None
        self.network_client = None
        self.is_host = False

        # State management
        self.states = {
            "MAIN_MENU": MainMenuView(self),
            "LOBBY": LobbyView(self),
            "STRATEGY": StrategyView(self),
            "COMBAT": CombatView(self)
        }
        self.current_state = "MAIN_MENU"
        self.active_state_obj = self.states[self.current_state]

    def run(self):
        """The main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            self.handle_events()
            self.update(dt)
            self.draw()

        self.shutdown()

    def handle_events(self):
        """Passes events to the active state."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            self.active_state_obj.handle_event(event)

    def update(self, dt):
        """Updates the active state."""
        self.active_state_obj.update(dt)

    def draw(self):
        """Draws the active state."""
        self.screen.fill(BLACK)  # Default background
        self.active_state_obj.draw(self.screen)
        pygame.display.flip()

    def change_state(self, new_state, data=None):
        """
        Changes the current game state and passes data between them.
        """
        if new_state in self.states:
            self.current_state = new_state
            self.active_state_obj = self.states[self.current_state]
            # Pass data to the new state's on_enter method
            self.active_state_obj.on_enter(data)
            print(f"Game State Changed to: {self.current_state}")
        else:
            print(f"Error: State '{new_state}' not found.")

    def start_server(self):
        self.network_server = NetworkServer()
        self.network_server.start()
        self.is_host = True

    def start_client(self, host_ip):
        self.network_client = NetworkClient(host=host_ip)
        return self.network_client.connect()

    def shutdown(self):
        """Properly closes network connections."""
        if self.network_client:
            self.network_client.disconnect()
        if self.network_server:
            self.network_server.stop()

