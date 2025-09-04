# networking.py
# A functional implementation of the client-server networking logic.

import socket
import pickle
import threading
import time
import random
import pygame
from settings import SHIP_STATS

HEADER_LENGTH = 10


class NetworkClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.player_id = None
        self.message_queue = []
        self.queue_lock = threading.Lock()
        print("Networking client initialized.")

    def connect(self):
        try:
            print(f"Attempting to connect to {self.host}:{self.port}...")
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            threading.Thread(target=self.listen_for_messages, daemon=True).start()
            print("Connection successful.")
            return True
        except socket.error as e:
            print(f"Connection failed: {e}")
            self.connected = False
            return False

    def listen_for_messages(self):
        while self.connected:
            try:
                message_header = self.client_socket.recv(HEADER_LENGTH)
                if not len(message_header):
                    print("Connection closed by server.")
                    self.connected = False
                    break

                message_length = int(message_header.decode('utf-8').strip())
                full_message = b''
                while len(full_message) < message_length:
                    chunk = self.client_socket.recv(message_length - len(full_message))
                    if not chunk: break
                    full_message += chunk

                message_data = pickle.loads(full_message)

                with self.queue_lock:
                    if message_data['type'] == 'welcome':
                        self.player_id = message_data['payload']['id']
                        print(f"Received welcome. My Player ID is {self.player_id}")
                    else:
                        self.message_queue.append(message_data)

            except Exception as e:
                print(f"Error receiving data: {e}")
                self.connected = False
                break

    def get_messages(self):
        """Returns all messages from the queue and clears it."""
        with self.queue_lock:
            messages = list(self.message_queue)
            self.message_queue.clear()
        return messages

    def send_commands(self, commands):
        if not self.connected:
            print("Not connected to server.")
            return
        message_data = {'type': 'client_commands', 'payload': commands}
        self.send_message(message_data)

    def send_message(self, message_data):
        try:
            message = pickle.dumps(message_data)
            header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.sendall(header + message)
        except socket.error as e:
            print(f"Failed to send message: {e}")
            self.connected = False

    def disconnect(self):
        if self.connected:
            self.connected = False
            self.client_socket.close()
            print("Disconnected from server.")


class NetworkServer:
    def __init__(self, host='0.0.0.0', port=5555, max_clients=4):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # conn: player_id
        self.client_commands = {}  # player_id: commands
        self.player_counter = 1
        self.running = False
        self.game_started = False
        self.game_state = {}
        self.world = None
        self.lobby_state = {'players': []}
        self.lock = threading.Lock()
        print("Networking server initialized.")

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            self.running = True
            print(f"Server starting on {self.host}:{self.port}")
            threading.Thread(target=self.accept_connections, daemon=True).start()
            threading.Thread(target=self.lobby_updater, daemon=True).start()
        except socket.error as e:
            print(f"Server failed to start: {e}")

    def lobby_updater(self):
        while self.running and not self.game_started:
            with self.lock:
                self.update_lobby_state()
                self.broadcast_message({'type': 'lobby_update', 'payload': self.lobby_state})
            time.sleep(1)

    def accept_connections(self):
        print("Server is waiting for connections...")
        while self.running:  # Allow connections even after game starts for reconnections (future)
            try:
                conn, addr = self.server_socket.accept()
                with self.lock:
                    if not self.game_started and len(self.clients) < self.max_clients:
                        player_id = self.player_counter
                        self.player_counter += 1

                        print(f"Accepted connection from {addr}, assigned Player ID {player_id}")
                        self.clients[conn] = player_id
                        self.client_commands[player_id] = []

                        self.send_message(conn, {'type': 'welcome', 'payload': {'id': player_id}})
                        threading.Thread(target=self.client_handler, args=(conn, addr), daemon=True).start()
                    else:
                        # Future: Handle reconnections or refuse connection
                        print(f"Refused connection from {addr}: Lobby full or game in progress.")
                        conn.close()
            except socket.error:
                break

    def client_handler(self, conn, addr):
        while self.running:
            try:
                message_header = conn.recv(HEADER_LENGTH)
                if not message_header: break

                message_length = int(message_header.decode('utf-8').strip())
                full_message = pickle.loads(conn.recv(message_length))

                player_id = self.clients.get(conn)
                if not player_id: continue

                if full_message['type'] == 'client_commands':
                    with self.lock:
                        self.client_commands[player_id] = full_message['payload']

                elif full_message['type'] == 'start_game_request':
                    if player_id == 1:
                        self.start_game()

            except (ConnectionResetError, EOFError, pickle.UnpicklingError):
                break

        print(f"Connection from {addr} closed.")
        with self.lock:
            player_id = self.clients.pop(conn, None)
            if player_id:
                self.client_commands.pop(player_id, None)
        conn.close()

    def update_lobby_state(self):
        self.lobby_state['players'] = [{'id': pid, 'addr': conn.getpeername()} for conn, pid in self.clients.items()]

    def start_game(self):
        from world import World

        with self.lock:
            if self.game_started:
                print("Start game request ignored: Game already started.")
                return
            self.game_started = True
            print("Initializing and broadcasting start_game state...")

            world_seed = random.randint(0, 10000)
            self.world = World(seed=world_seed)
            start_positions = self.world.valid_start_islands

            self.game_state = {'world_seed': world_seed, 'units': {}, 'turn_number': 0}
            unit_id_counter = 0

            player_ids = list(self.client_commands.keys())
            random.shuffle(player_ids)

            for i, player_id in enumerate(player_ids):
                if i < len(start_positions):
                    pos = start_positions[i]
                    for unit_type in ['command_center', 'cruiser', 'scout']:
                        unit_id = unit_id_counter
                        unit_pos = (pos[0] + random.randint(-20, 20), pos[1] + random.randint(-20, 20))

                        unit_state = {
                            'id': unit_id, 'type': unit_type, 'owner': player_id,
                            'pos': unit_pos, 'hp': SHIP_STATS[unit_type]['hp'],
                            'target_pos': unit_pos
                        }
                        self.game_state['units'][unit_id] = unit_state
                        unit_id_counter += 1

            self.broadcast_message({'type': 'start_game', 'payload': self.game_state})
            threading.Thread(target=self.game_loop, daemon=True).start()

    def game_loop(self):
        turn_duration = 1.0
        print("Server game loop is running.")
        while self.running:
            turn_start_time = time.time()
            with self.lock:
                self.process_commands()
                self.update_game_state()
                self.broadcast_message({'type': 'game_update', 'payload': self.game_state})

            elapsed_time = time.time() - turn_start_time
            sleep_time = turn_duration - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    def process_commands(self):
        for player_id, commands in self.client_commands.items():
            if commands:
                for command in commands:
                    unit_id = command.get('unit_id')
                    unit = self.game_state['units'].get(unit_id)
                    if unit and unit['owner'] == player_id:
                        if command['action'] == 'move' and unit['type'] != 'command_center':
                            unit['target_pos'] = command['target']
        for pid in self.client_commands: self.client_commands[pid] = []

    def update_game_state(self):
        self.game_state['turn_number'] += 1
        for uid, unit in self.game_state['units'].items():
            if unit['type'] == 'command_center': continue
            current_pos = pygame.math.Vector2(unit['pos'])
            target_pos = pygame.math.Vector2(unit['target_pos'])
            if current_pos.distance_to(target_pos) < 1: continue
            direction = (target_pos - current_pos).normalize()
            speed = SHIP_STATS[unit['type']]['speed']
            new_pos = current_pos + direction * speed
            if not self.world.is_land(new_pos):
                unit['pos'] = (new_pos.x, new_pos.y)
            else:
                unit['target_pos'] = unit['pos']

    def broadcast_message(self, message_data):
        for client_conn in list(self.clients.keys()):
            self.send_message(client_conn, message_data)

    def send_message(self, conn, message_data):
        try:
            message = pickle.dumps(message_data)
            header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            conn.sendall(header + message)
        except socket.error:
            pass

    def stop(self):
        self.running = False
        for client in self.clients: client.close()
        self.server_socket.close()
        print("Server stopped.")

