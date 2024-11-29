import threading
import socket
import json
import time
import unittest

from Server.server import start_server
from Client.config import HOST, PORT, BUFFER_SIZE


class TestRegistration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the server in a separate thread
        cls.server_thread = threading.Thread(target=start_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)  # Give the server some time to start

    def test_registration(self):
        # Simulate the client registration process
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))

            # Prepare registration data
            registration_data = {
                "first_name": "foo",
                "last_name": "bar",
                "phone_number": "054567891",
                "password": "123456"
            }
            data = json.dumps(registration_data)

            # Send registration data
            client_socket.sendall(data.encode('utf-8'))

            # Receive and verify the server's response
            response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            self.assertEqual(response, "Registration successful")


if __name__ == "__main__":
    unittest.main()