import json
import unittest
from unittest.mock import Mock, patch
from Server.Handlers.LoginHandler import LoginHandler
from Server.Handlers.SendMessageHandler import SendMessageHandler
from Server.Handlers.ReceiveMessageHandler import ReceiveMessage

class TestLoginHandler(unittest.TestCase):
    def setUp(self):
        self.db_manager = Mock()
        self.clients = Mock()
        self.send_message_handler = Mock(spec=SendMessageHandler)
        self.receive_message_handler = Mock(spec=ReceiveMessage)
        self.login_handler = LoginHandler(self.db_manager, self.clients)

    def test_handle_login_success(self):
        payload = json.dumps({
            "phone_number": "1234567890",
            "password": "correct_password"
        })
        client_address = ("127.0.0.1", 12345)
        connection = Mock()

        self.db_manager.get_user_by_phone_number.return_value = {
            "phone_number": "1234567890",
            "password": "correct_password"
        }
        self.db_manager.get_offline_messages.return_value = [
            {"sender": "0987654321", "message": "Hello!"}
        ]

        response = self.login_handler.handle_login(payload, client_address, connection)

        self.assertEqual(response, "SUCCESS: Offline messages sent.")
        self.clients.add_connected_user.assert_called_with("1234567890", connection)

    def test_handle_login_invalid_json(self):
        payload = "invalid_json"
        client_address = ("127.0.0.1", 12345)
        connection = Mock()

        response = self.login_handler.handle_login(payload, client_address, connection)

        self.assertEqual(response, "ERROR: Invalid JSON format.")

    def test_handle_login_missing_data(self):
        payload = json.dumps({
            "phone_number": "1234567890"
        })
        client_address = ("127.0.0.1", 12345)
        connection = Mock()

        response = self.login_handler.handle_login(payload, client_address, connection)

        self.assertEqual(response, "ERROR: Missing login data.")

    def test_handle_login_user_not_found(self):
        payload = json.dumps({
            "phone_number": "1234567890",
            "password": "correct_password"
        })
        client_address = ("127.0.0.1", 12345)
        connection = Mock()

        self.db_manager.get_user_by_phone_number.return_value = None

        response = self.login_handler.handle_login(payload, client_address, connection)

        self.assertEqual(response, "ERROR: User not found.")

    def test_handle_login_incorrect_password(self):
        payload = json.dumps({
            "phone_number": "1234567890",
            "password": "wrong_password"
        })
        client_address = ("127.0.0.1", 12345)
        connection = Mock()

        self.db_manager.get_user_by_phone_number.return_value = {
            "phone_number": "1234567890",
            "password": "correct_password"
        }

        response = self.login_handler.handle_login(payload, client_address, connection)

        self.assertEqual(response, "ERROR: Incorrect password.")

if __name__ == '__main__':
    unittest.main()