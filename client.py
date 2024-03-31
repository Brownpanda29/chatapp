import socket
import threading
import os

# Function to handle receiving messages from server
def receive_messages(client_socket):
    while True:
        try:
            # Receive data from server
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode())
        except ConnectionResetError:
            break

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Define host and port
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    # Connect to server
    client_socket.connect((HOST, PORT))

    # Send client's name to server
    client_name = input("Enter your name: ")
    client_socket.sendall(client_name.encode())

    # Start a thread to receive messages from server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Main loop to send messages to server
    while True:
        # Get message from user input
        message = input()

        # Send data to server
        client_socket.sendall(message.encode())
