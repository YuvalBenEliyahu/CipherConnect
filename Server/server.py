import socket
import threading
import logging
import json

from Server.Database.Clients import Clients
from Server.Database.Database import DatabaseManager
from Server.Handlers.ReceiveMessageHandler import ReceiveMessageHandler

from Server.Handlers.RegistrationHandler import RegistrationHandler
from Server.Handlers.SendMessageHandler import SendMessageHandler
from Server.config import HOST, PORT, BUFFER_SIZE
from Server.Handlers.LoginHandler import LoginHandler

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the database and handlers
db_manager = DatabaseManager()
clients = Clients(db_manager)
registration_handler = RegistrationHandler(db_manager, clients)
login_handler = LoginHandler(db_manager, clients)
send_message_handler = SendMessageHandler(db_manager, clients)
receive_message_handler = ReceiveMessageHandler(clients, send_message_handler)

def handle_client(client_socket, client_address):
    try:
        data = client_socket.recv(BUFFER_SIZE).decode()
        if not data:
            return

        # Parse JSON data
        try:
            request = json.loads(data)
        except json.JSONDecodeError:
            client_socket.send("ERROR: Invalid JSON format.".encode())
            return

        type = request.get("type")
        payload = request.get("data")

        if not type or not payload:
            client_socket.send("ERROR: Missing type or payload.".encode())
            return

        # Handle the type
        if type == "REGISTER":
            payload_json = json.dumps(payload)
            response = registration_handler.handle_registration(payload_json, client_address)
            client_socket.send(response.encode())
        elif type == "LOGIN":
            payload_json = json.dumps(payload)
            response = login_handler.handle_login(payload_json, client_address, client_socket)
            client_socket.send(response.encode())
        elif type == "MESSAGE":
            payload_json = json.dumps(payload)
            response = receive_message_handler.handle_message(client_socket, payload_json)
            client_socket.send(response.encode())
        else:
            client_socket.send(f"ERROR: Unknown type '{type}'.".encode())
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