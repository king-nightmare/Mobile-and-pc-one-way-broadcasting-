import socket

# 1. Create the UDP socket outside the loop
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Broadcast chat started! Type 'exit' to quit.\n")

# 2. Loop indefinitely until stopped
while True:
    # Get the message from the user
    message = input("Type your broadcast message: ")
    
    # Check if the user wants to quit
    if message.lower() == 'exit':
        print("Closing connection...")
        break  # Breaks out of the while loop
        
    # Skip sending if the user just pressed Enter without typing anything
    if not message.strip():
        continue

    # 3. Send the message
    sock.sendto(message.encode('utf-8'), ("255.255.255.255", 50000))
    print("-> Sent!")

# 4. Clean up and close the socket after exiting the loop
sock.close()
print("Socket closed. Goodbye!")
