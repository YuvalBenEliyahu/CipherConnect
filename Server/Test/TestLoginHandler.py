import json
import unittest
from unittest.mock import Mock
from Server.Handlers.LoginHandler import LoginHandler
from Server.Handlers.SendMessageHandler import SendMessageHandler

class TestLoginHandler(unittest.TestCase):
    def setUp(self):
        self.db_manager = Mock()
        self.clients = Mock()
        self.send_message_handler = Mock(spec=SendMessageHandler)
        self.login_handler = LoginHandler(self.db_manager, self.clients, self.send_message_handler)

    def test_handle_login_success(self):
        data = {
            "phone_number": "1234567890",
            "password": "correct_password"
        }
        client_address = ("127.0.0.1", 12345)
        connection = Mock()

        self.db_manager.get_user_by_phone_number.return_value = {
            "phone_number": "1234567890",
            "password": "correct_password"
        }

        self.login_handler.handle(data, client_address, connection)

        self.send_message_handler.send_response.assert_called_with(connection, "LOGIN_SUCCESS", "Login successful.")
        self.clients.add_connected_user.assert_called_with("1234567890", connection)

    def test_handle_login_missing_data(self):
        data = {
            "phone_number": "1234567890"
        }
        client_address = ("127.0.0.1", 12345)
        connection = Mock()

        self.login_handler.handle(data, client_address, connection)

        self.send_message_handler.send_response.assert_called_with(connection, "ERROR", "Missing login data.")

    def test_handle_login_user_not_found(self):
        data = {
            "phone_number": "1234567890",
            "password": "correct_password"
        }
        client_address = ("127.0.0.1", 12345)
        connection = Mock()

        self.db_manager.get_user_by_phone_number.return_value = None

        self.login_handler.handle(data, client_address, connection)

        self.send_message_handler.send_response.assert_called_with(connection, "ERROR", "User not found.")

    def test_handle_login_incorrect_password(self):
        data = {
            "phone_number": "1234567890",
            "password": "wrong_password"
        }
        client_address = ("127.0.0.1", 12345)
        connection = Mock()

        self.db_manager.get_user_by_phone_number.return_value = {
            "phone_number": "1234567890",
            "password": "correct_password"
        }

        self.login_handler.handle(data, client_address, connection)

        self.send_message_handler.send_response.assert_called_with(connection, "ERROR", "Incorrect password.")

if __name__ == '__main__':
    unittest.main()