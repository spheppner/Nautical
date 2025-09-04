# networking.py
# A functional implementation of the client-server networking logic.

import socket
import pickle
import threading
import time

HEADER_LENGTH = 10


class NetworkClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.last_message = None
        self.connected = False
        self.player_id = None
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
                if message_data['type'] == 'welcome':
                    self.player_id = message_data['payload']['id']
                    print(f"Received welcome. My Player ID is {self.player_id}")
                else:
                    self.last_message = message_data

            except Exception as e:
                print(f"Error receiving data: {e}")
                self.connected = False
                break

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
        self.client_data = {}  # conn: data
        self.player_counter = 1
        self.running = False
        self.lobby_state = {'players': []}
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
        """Periodically sends the lobby state to all clients."""
        while self.running:
            self.update_lobby_state()
            self.broadcast_message({'type': 'lobby_update', 'payload': self.lobby_state})
            time.sleep(1)  # Send update every second

    def accept_connections(self):
        print("Server is waiting for connections...")
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                if len(self.clients) < self.max_clients:
                    player_id = self.player_counter
                    self.player_counter += 1

                    print(f"Accepted connection from {addr}, assigned Player ID {player_id}")
                    self.clients[conn] = player_id
                    self.client_data[conn] = None

                    # Send welcome message
                    welcome_msg = {'type': 'welcome', 'payload': {'id': player_id}}
                    self.send_message(conn, welcome_msg)

                    threading.Thread(target=self.client_handler, args=(conn, addr), daemon=True).start()
                else:
                    print(f"Refused connection from {addr}: Server is full.")
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
                self.client_data[conn] = full_message['payload']

            except (ConnectionResetError, EOFError, pickle.UnpicklingError):
                break

        print(f"Connection from {addr} closed.")
        player_id = self.clients.pop(conn, None)
        self.client_data.pop(conn, None)
        conn.close()
        self.update_lobby_state()

    def update_lobby_state(self):
        self.lobby_state['players'] = [{'id': pid, 'addr': conn.getpeername()} for conn, pid in self.clients.items()]

    def broadcast_message(self, message_data):
        if not self.clients: return
        for client_conn in list(self.clients.keys()):
            self.send_message(client_conn, message_data)

    def send_message(self, conn, message_data):
        try:
            message = pickle.dumps(message_data)
            header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            conn.sendall(header + message)
        except socket.error:
            # Client disconnected, will be handled by its handler thread
            pass

    def stop(self):
        self.running = False
        for client in self.clients:
            client.close()
        # self.server_socket.shutdown(socket.SHUT_RDWR) # More forceful
        self.server_socket.close()
        print("Server stopped.")

