import socket
import threading
import logging
from Server.Database.Database import DatabaseManager
from Server.Handlers.RegistrationHandler import RegistrationHandler
from Server.config import HOST, PORT, BUFFER_SIZE

# Initialize the database and handlers
db_manager = DatabaseManager()
registration_handler = RegistrationHandler(db_manager)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(client_socket):
    try:
        # Receive data from the client
        data = client_socket.recv(BUFFER_SIZE).decode()
        if not data:
            return

        # Split the data into command and payload
        parts = data.split("|", 1)
        if len(parts) != 2:
            client_socket.send("ERROR: Invalid data format.".encode())
            return

        command, payload = parts[0], parts[1]

        # Handle the command
        if command == "REGISTER":
            response = registration_handler.handle_registration(payload)
            client_socket.send(response.encode())
        else:
            client_socket.send(f"ERROR: Unknown command '{command}'.".encode())
    except KeyError as e:
        logging.error(f"KeyError: {e}")
        client_socket.send(f"ERROR: KeyError - {str(e)}".encode())
    except Exception as e:
        logging.error(f"Exception: {e}")
        client_socket.send(f"ERROR: {str(e)}".encode())
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    logging.info(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        logging.info(f"New connection from {client_address}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()