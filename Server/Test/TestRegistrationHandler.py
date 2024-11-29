# Python
import unittest
from Server.Handlers.RegistrationHandler import RegistrationHandler
from unittest.mock import Mock

class TestRegistrationHandler(unittest.TestCase):
    def setUp(self):
        self.mock_db_manager = Mock()
        self.registration_handler = RegistrationHandler(self.mock_db_manager)

    def test_handle_registration_success(self):
        self.mock_db_manager.add_user.return_value = "User John Doe added successfully."
        payload = "John,Doe,1234567890,password123,public_key"
        response = self.registration_handler.handle_registration(payload)
        self.assertEqual(response, "SUCCESS: User John Doe registered.")

    def test_handle_registration_phone_exists(self):
        self.mock_db_manager.add_user.return_value = "Error: Phone number already exists."
        payload = "John,Doe,1234567890,password123,public_key"
        response = self.registration_handler.handle_registration(payload)
        self.assertEqual(response, "Error: Phone number already exists.")

    def test_handle_registration_invalid_format(self):
        payload = "John,Doe,1234567890"
        response = self.registration_handler.handle_registration(payload)
        self.assertEqual(response, "ERROR: Invalid registration data format.")

if __name__ == '__main__':
    unittest.main()