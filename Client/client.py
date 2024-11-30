import socket
import sys

from Client.Handlers.login_handler import login
from Client.Handlers.message_handler import send_message
from Client.Handlers.register_handler import register
from Client.config import PORT, HOST


def start_client(host=HOST, port=PORT):
    """Start the client and process CLI commands."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            while True:
                # Display menu
                print("\nOptions:")
                print("1. Register")
                print("2. Login")
                print("3. Send message")
                option = input("Choose an option (1/2/3): ")

                if option == "1":
                    register(client_socket)
                elif option == "2":
                    login(client_socket)
                elif option == "3":
                    send_message(client_socket)
                else:
                    print("Invalid option. Please try again.")
        except ConnectionRefusedError:
            print(f"Could not connect to server at {host}:{port}")
            sys.exit(1)
