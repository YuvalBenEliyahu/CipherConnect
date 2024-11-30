import socket
import sys
import threading

from Client.Handlers.login_handler import login
from Client.Handlers.chat_handler import navigate_chats, receive_messages
from Client.Handlers.register_handler import register
from Client.config import PORT, HOST


def start_client(host=HOST, port=PORT):
    """Start the client and process CLI commands."""
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((host, port))
                print(f"Connected to server at {host}:{port}")

                # Start a thread to receive messages
                receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
                receive_thread.daemon = True
                receive_thread.start()

                while True:
                    # Display menu
                    print("\nOptions:")
                    print("1. Register")
                    print("2. Login")
                    print("3. Chat")
                    option = input("Choose an option (1/2/3): ")

                    if option == "1":
                        register(client_socket)
                        break
                    elif option == "2":
                        login(client_socket)
                        break
                    elif option == "3":
                        navigate_chats(client_socket)
                    else:
                        print("Invalid option. Please try again.")
            except ConnectionRefusedError:
                print(f"Could not connect to server at {host}:{port}")
                sys.exit(1)
            except ConnectionAbortedError as e:
                print(f"Connection was aborted: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                print("Closing the client socket.")