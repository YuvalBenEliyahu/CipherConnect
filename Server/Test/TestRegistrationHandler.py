import os
import unittest
import json

from Server.Handlers.RegistrationHandler import RegistrationHandler
from unittest.mock import Mock

from Server.Test.TestUtils import generate_public_key

class TestRegistrationHandler(unittest.TestCase):
    def setUp(self):
        self.mock_db_manager = Mock()
        self.registration_handler = RegistrationHandler(self.mock_db_manager)
        # Delete the users.db file if it exists
        db_path = os.path.join(os.path.dirname(__file__), 'users.db')
        if os.path.exists(db_path):
            os.remove(db_path)

    def test_handle_registration_success(self):
        self.mock_db_manager.add_user.return_value = "User John Doe added successfully."
        public_key_pem = generate_public_key()
        payload = json.dumps({
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "password": "Password1$",
            "public_key": public_key_pem
        })
        response = self.registration_handler.handle_registration(payload)
        self.assertEqual(response, "SUCCESS: User John Doe registered.")

    def test_handle_registration_phone_exists(self):
        self.mock_db_manager.add_user.return_value = "Error: Phone number already exists."
        public_key_pem = generate_public_key()
        payload = json.dumps({
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "password": "Password1$",
            "public_key": public_key_pem
        })
        response = self.registration_handler.handle_registration(payload)
        self.assertEqual(response, "Error: Phone number already exists.")

    def test_handle_registration_invalid_format(self):
        payload = json.dumps({
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890"
        })
        response = self.registration_handler.handle_registration(payload)
        self.assertEqual(response, "ERROR: Missing registration data.")

    def test_handle_registration_invalid_name(self):
        public_key_pem = generate_public_key()
        payload = json.dumps({
            "first_name": "John123",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "password": "Password1$",
            "public_key": public_key_pem
        })
        response = self.registration_handler.handle_registration(payload)
        self.assertEqual(response, "ERROR: Invalid name format.")

    def test_handle_registration_invalid_last_name(self):
        public_key_pem = generate_public_key()
        payload = json.dumps({
            "first_name": "John",
            "last_name": "Doe123",
            "phone_number": "1234567890",
            "password": "Password1$",
            "public_key": public_key_pem
        })
        response = self.registration_handler.handle_registration(payload)
        self.assertEqual(response, "ERROR: Invalid last name format.")

    def test_handle_registration_invalid_phone_number(self):
        public_key_pem = generate_public_key()
        payload = json.dumps({
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "12345",
            "password": "Password1$",
            "public_key": public_key_pem
        })
        response = self.registration_handler.handle_registration(payload)
        self.assertEqual(response, "ERROR: Invalid phone number format.")

    def test_handle_registration_invalid_password(self):
        public_key_pem = generate_public_key()
        payload = json.dumps({
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "password": "pass",
            "public_key": public_key_pem
        })
        response = self.registration_handler.handle_registration(payload)
        self.assertEqual(response, "ERROR: Invalid password format.")

    def test_handle_registration_invalid_public_key(self):
        payload = json.dumps({
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "password": "Password1$",
            "public_key": "invalid_key"
        })
        response = self.registration_handler.handle_registration(payload)
        self.assertEqual(response, "ERROR: Invalid public key format.")

if __name__ == '__main__':
    unittest.main()