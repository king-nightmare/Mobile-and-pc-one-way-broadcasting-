import socket

# 1. Create a UDP socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Allow multiple applications to use the same port number
client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 3. Bind the socket to all available network interfaces ('') and port 50000
client_sock.bind(('', 50000))

print("Listening for broadcast messages on port 50000...")
print("Press Ctrl+C to stop.\n")

# 4. Continuously listen for incoming data
try:
    while True:
        # recvfrom blocks and waits until a message arrives
        # It returns a tuple: (data_bytes, (sender_ip, sender_port))
        data, addr = client_sock.recvfrom(1024)

        # Decode the bytes back into a readable string
        decoded_message = data.decode('utf-8')

        print(f"[{addr[0]}]: {decoded_message}")

except KeyboardInterrupt:
    print("\nStopping client listener...")

finally:
    client_sock.close()
    print("Client socket closed.")
