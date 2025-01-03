import queue
import socket
import threading
from Client.Handlers.login_handler import login
from Client.Handlers.chat_handler import navigate_chats
from Client.Handlers.register_handler import register
from Client.Handlers.server_comunication_handler import receive_server_messages
from Client.encryption import generate_or_load_ec_keypair, serialize_public_key
from Client.queue_manager import message_queue


def start_client(host, port, db_manager, private_key_file, public_key_file):
    """Start the client and process CLI commands."""

    # Generate key pair for the client
    private_key, public_key = generate_or_load_ec_keypair(private_key_file, public_key_file)
    public_key_pem = serialize_public_key(public_key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            receive_thread = threading.Thread(
                target=receive_server_messages,
                args=(client_socket, db_manager, private_key),
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
                    register(client_socket, public_key_pem)
                elif option == "2":
                    if login(client_socket):
                        navigate_chats(client_socket, db_manager, private_key)
                elif option == "3":
                    print("Exiting.")
                    break
                else:
                    print("Invalid option. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Closing the client socket.")



