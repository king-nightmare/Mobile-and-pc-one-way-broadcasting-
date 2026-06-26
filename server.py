import socket
import threading
import time
from datetime import datetime


class BroadcastServer:
    def __init__(self, host="0.0.0.0", port=5000, discovery_port=5001):
        self.host = host
        self.port = port
        self.discovery_port = discovery_port
        self.clients = set()
        self.clients_lock = threading.Lock()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.settimeout(1)

        self.running = False

    def get_local_ip(self):
        """Get local network IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def start(self):
        """Start background services"""
        if self.running:
            print("Server already running.")
            return

        self.running = True

        threading.Thread(
            target=self.broadcast_discovery,
            daemon=True
        ).start()

        threading.Thread(
            target=self.listen_for_clients,
            daemon=True
        ).start()

        print(
            f"Server started on {self.get_local_ip()}:{self.port}"
        )

    def broadcast_discovery(self):
        """Broadcast server discovery packets"""
        discovery_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        discovery_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_BROADCAST,
            1
        )

        local_ip = self.get_local_ip()

        while self.running:
            try:
                msg = f"DISCOVER:{local_ip}:{self.port}"

                discovery_socket.sendto(
                    msg.encode("utf-8"),
                    ("255.255.255.255", self.discovery_port)
                )

                time.sleep(2)

            except Exception as e:
                print("Discovery error:", e)

    def listen_for_clients(self):
        """Listen for REGISTER messages"""
        while self.running:
            try:
                data, addr = self.server_socket.recvfrom(1024)

                message = data.decode("utf-8").strip()

                if message == "REGISTER":
                    with self.clients_lock:
                        self.clients.add(addr)

                    print(f"Client registered: {addr}")

                    self.server_socket.sendto(
                        b"REGISTERED",
                        addr
                    )

            except socket.timeout:
                continue

            except Exception as e:
                if self.running:
                    print("Listener error:", e)

    def broadcast_message(self, message):
        """Send a message to all clients"""

        if not self.running:
            print("Server is not running.")
            return

        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}"

        with self.clients_lock:
            clients = list(self.clients)

        if not clients:
            print("No clients connected.")
            return

        for client in clients:
            try:
                self.server_socket.sendto(
                    full_message.encode("utf-8"),
                    client
                )

            except Exception as e:
                print(f"Failed to send to {client}: {e}")

                with self.clients_lock:
                    self.clients.discard(client)

        print(f"Broadcasted: {full_message}")

    def list_clients(self):
        with self.clients_lock:
            return list(self.clients)

    def stop(self):
        self.running = False

        try:
            self.server_socket.close()
        except Exception:
            pass

        print("Server stopped.")
        
