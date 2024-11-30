import socket
import threading
import logging
import json

from Server.Database.Clients import Clients
from Server.Database.Database import DatabaseManager
from Server.Handlers.MessageHandler import MessageHandler
from Server.config import HOST, PORT, BUFFER_SIZE

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the database manager and clients
db_manager = DatabaseManager()
clients = Clients(db_manager)

# Create an instance of MessageHandler
message_handler = MessageHandler(db_manager, clients)

def handle_client(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE).decode()
            if not data:
                break

            # Parse JSON data
            try:
                request = json.loads(data)
            except json.JSONDecodeError:
                client_socket.send("ERROR: Invalid JSON format.".encode())
                continue

            # Handle the message using the MessageHandler instance
            message_handler.handle_message(request, client_socket, client_address)

    except KeyError as e:
        logging.error(f"KeyError: {e}")
        client_socket.send(f"ERROR: KeyError - {str(e)}".encode())
    except Exception as e:
        logging.error(f"Exception: {e}")
        client_socket.send(f"ERROR: {str(e)}".encode())
    finally:
        logging.debug("Closing client socket for address: %s", client_address)
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    logging.info(f"Server is listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            logging.info(f"New connection from {client_address}")
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    except Exception as e:
        logging.error(f"Server encountered an error: {e}")
    finally:
        server_socket.close()
        logging.info("Server has been shut down.")