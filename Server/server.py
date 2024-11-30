import socket
import threading
import logging
from Server.Database.Database import DatabaseManager
from Server.Handlers.RegistrationHandler import RegistrationHandler

from Server.config import HOST, PORT, BUFFER_SIZE
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


from Server.Handlers.login_handler import LoginHandler

# Initialize the database and handlers
db_manager = DatabaseManager()
registration_handler = RegistrationHandler(db_manager)
login_handler = LoginHandler(db_manager)

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

        command = request.get("command")
        payload = request.get("data")

        if not command or not payload:
            client_socket.send("ERROR: Missing command or payload.".encode())
            return

        # Handle the command
        if command == "REGISTER":
            payload_json = json.dumps(payload)
            response = registration_handler.handle_registration(payload_json, client_address)
            client_socket.send(response.encode())
        elif command == "LOGIN":
            payload_json = json.dumps(payload)
            response = login_handler.handle_login(payload_json, client_address)
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

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            logging.info(f"New connection from {client_address}")
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address, server_socket))
            thread.start()
    except Exception as e:
        logging.error(f"Server encountered an error: {e}")
    finally:
        server_socket.close()
        logging.info("Server has been shut down.")
