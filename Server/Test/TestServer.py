import unittest
import socket
import threading
from Server.server import start_server
from Server.config import HOST, PORT, BUFFER_SIZE

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=start_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    def test_server_registration(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((HOST, PORT))
            registration_data = "REGISTER|John,Doe,1234567890,password123,public_key"
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