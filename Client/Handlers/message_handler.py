from Client.config import BUFFER_SIZE


def send_message(client_socket):
    """Send a message to the server."""
    message = input("Enter your message: ")
    client_socket.sendall(f"MESSAGE {message}".encode('utf-8'))
    response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    print(f"Server response: {response}")