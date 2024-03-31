import socket
import threading

# Global variable to hold client connections
clients = {}

# Function to handle receiving messages from clients
def handle_client(client_socket, client_address, client_name):
    while True:
        # Receive data from client
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            # Broadcast the message to all other clients
            broadcast_message(client_name, data)
        except ConnectionResetError:
            break

    # Remove the client from the list when they disconnect
    del clients[client_name]
    print(f"Client {client_name} disconnected")
    client_socket.close()

# Function to broadcast message to all clients except sender
def broadcast_message(sender_name, message):
    message_with_name = f"{sender_name}: {message.decode()}"
    for name, client_socket in clients.items():
        if name != sender_name:
            try:
                client_socket.sendall(message_with_name.encode())
            except ConnectionResetError:
                del clients[name]

# Function to send announcement to all clients
def send_announcement(message):
    announcement = f"[Server Announcement] : {message}"
    for client_socket in clients.values():
        try:
            client_socket.sendall(announcement.encode())
        except ConnectionResetError:
            pass

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Define host and port
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on

    # Bind the socket to the address
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print("Server is listening for connections...")

    while True:
        # Accept connections
        client_socket, client_address = server_socket.accept()

        # Receive the client's name
        client_name = client_socket.recv(1024).decode()

        # Add the client to the dictionary
        clients[client_name] = client_socket
        print(f"Client {client_name} connected from {client_address}")

        # Send announcement to all clients
        send_announcement(f"{client_name} entered the chat.")

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_name))
        client_thread.start()
