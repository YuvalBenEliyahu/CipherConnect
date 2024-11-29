# Python
import unittest
import socket
import threading
import os
import time

from Server.Test.TestUtils import generate_public_key
from Server.server import start_server
from Server.config import HOST, PORT, BUFFER_SIZE


class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Delete the users.db file if it exists
        db_path = os.path.join(os.path.dirname(__file__), 'users.db')
        if os.path.exists(db_path):
            os.remove(db_path)

        cls.server_thread = threading.Thread(target=start_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    def test_server_registration(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((HOST, PORT))
            public_key_pem = generate_public_key()
            # Use a valid password format
            registration_data = f"REGISTER|John,Doe,1234567890,Password1$,{public_key_pem}"
            client_socket.sendall(registration_data.encode('utf-8'))
            response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            self.assertEqual(response, "SUCCESS: User John Doe registered.")
        finally:
            client_socket.close()

    def test_server_invalid_command(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((HOST, PORT))
            invalid_data = "INVALID|Some data"
            client_socket.sendall(invalid_data.encode('utf-8'))
            response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            self.assertEqual(response, "ERROR: Unknown command 'INVALID'.")
        finally:
            client_socket.close()

if __name__ == '__main__':
    unittest.main()