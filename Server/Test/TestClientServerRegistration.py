import os
import socket
import threading
import unittest
import json

from Server.Test.TestUtils import generate_public_key
from Server.config import HOST, PORT, BUFFER_SIZE
from Server.server import start_server
from Client.config import ENCODE

import time

class TestClientServerRegistration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Delete the users.db file if it exists
        db_path = os.path.join(os.path.dirname(__file__), 'users.db')
        if os.path.exists(db_path):
            os.remove(db_path)

        cls.server_thread = threading.Thread(target=start_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)  # Give the server some time to start

    @classmethod
    def tearDownClass(cls):
        # Ensure the server is stopped
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((HOST, PORT))
            shutdown_command = json.dumps({"command": "SHUTDOWN"})
            client_socket.sendall(shutdown_command.encode(ENCODE))
        finally:
            client_socket.close()
        cls.server_thread.join()

    def test_registration(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((HOST, PORT))
            public_key_pem = generate_public_key()
            registration_data = json.dumps({
                "command": "REGISTER",
                "data": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_number": "1234567890",
                    "password": "Password1$",
                    "public_key": public_key_pem
                }
            })
            client_socket.sendall(registration_data.encode(ENCODE))
            response = client_socket.recv(BUFFER_SIZE).decode(ENCODE)
            self.assertEqual(response, "SUCCESS: User John Doe registered.")
        finally:
            client_socket.close()

    def test_registration_existing_user(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((HOST, PORT))
            public_key_pem = generate_public_key()
            registration_data = json.dumps({
                "command": "REGISTER",
                "data": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_number": "1234567890",
                    "password": "Password1$",
                    "public_key": public_key_pem
                }
            })
            client_socket.sendall(registration_data.encode(ENCODE))
            response = client_socket.recv(BUFFER_SIZE).decode(ENCODE)
            self.assertEqual(response, "ERROR: Phone number already exists.")
        finally:
            client_socket.close()

if __name__ == '__main__':
    unittest.main()