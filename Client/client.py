import queue
import socket
import threading
from Client.Handlers.login_handler import login
from Client.Handlers.chat_handler import navigate_chats
from Client.Handlers.register_handler import register
from Client.Handlers.server_comunication_handler import receive_server_messages
from Client.queue_manager import message_queue
from Client.config import PORT, HOST


def start_client(host=HOST, port=PORT, db_manager=None):
    """Start the client and process CLI commands."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            receive_thread = threading.Thread(
                target=receive_server_messages,
                args=(client_socket, db_manager),
                daemon=True
            )
            receive_thread.start()

            while True:
                try:
                    message_data = message_queue.get(timeout=0.1)
                    print(f"\nNew message: {message_data.get('message')}")
                except queue.Empty:
                    pass

                print("\nOptions:")
                print("1. Register")
                print("2. Login")
                print("3. Exit")
                option = input("Choose an option (1/2/3): ")

                if option == "1":
                    register(client_socket)
                elif option == "2":
                    if login(client_socket):
                        post_login_screen(client_socket, db_manager)
                elif option == "3":
                    print("Exiting.")
                    break
                else:
                    print("Invalid option. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Closing the client socket.")

def post_login_screen(client_socket, db_manager):
    while True:
        print("1. Chat")
        print("2. Logout")
        option = input("Choose an option (1/2): ")

        if option == "1":
            navigate_chats(client_socket, db_manager)
        elif option == "2":
            print("Logging out.")
            break
        else:
            print("Invalid option. Please try again.")