import re
from Server.utils import password_check, validate_public_key
import json

class RegistrationHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager


    def handle_registration(self, payload):
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return "ERROR: Invalid JSON format."

        name = data.get("first_name")
        last_name = data.get("last_name")
        phone_number = data.get("phone_number")
        password = data.get("password")
        public_key = data.get("public_key")

        if not name or not last_name or not phone_number or not password or not public_key:
            return "ERROR: Missing registration data."

        # Validate name (only letters and spaces)
        if not re.match(r'^[A-Za-z\s]+$', name):
            return "ERROR: Invalid name format."

        if not re.match(r'^[A-Za-z\s]+$', last_name):
            return "ERROR: Invalid last name format."

        # Validate phone number (only digits, length 10)
        if not re.match(r'^\d{10}$', phone_number):
            return "ERROR: Invalid phone number format."

        # Validate password using password_check function
        if not password_check(password):
            return "ERROR: Invalid password format."

        # Validate public key using validate_public_key function
        if not validate_public_key(public_key):
            return "ERROR: Invalid public key format."

        # Add user to the database
        result = self.db_manager.add_user(name, last_name, phone_number, password, public_key)
        if "Error" in result:
            return result
        else:
            return f"SUCCESS: User {name} {last_name} registered."