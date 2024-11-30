import re
import json
import logging
from Server.utils import password_check, validate_public_key

class RegistrationHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def handle_registration(self, payload, client_address):
        logging.debug("Handling registration with payload: %s from %s", payload, client_address)
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            logging.error("Invalid JSON format from %s", client_address)
            return "ERROR: Invalid JSON format."

        name = data.get("first_name")
        last_name = data.get("last_name")
        phone_number = data.get("phone_number")
        password = data.get("password")
        public_key = data.get("public_key")

        if not name or not last_name or not phone_number or not password or not public_key:
            logging.error("Missing registration data from %s", client_address)
            return "ERROR: Missing registration data."

        # Validate name (only letters and spaces)
        if not re.match(r'^[A-Za-z\s]+$', name):
            logging.error("Invalid name format from %s", client_address)
            return "ERROR: Invalid name format."

        if not re.match(r'^[A-Za-z\s]+$', last_name):
            logging.error("Invalid last name format from %s", client_address)
            return "ERROR: Invalid last name format."

        # Validate phone number (only digits, length 10)
        if not re.match(r'^\d{10}$', phone_number):
            logging.error("Invalid phone number format from %s", client_address)
            return "ERROR: Invalid phone number format."

        # Validate password using password_check function
        if not password_check(password):
            logging.error("Invalid password format from %s", client_address)
            return "ERROR: Invalid password format."

        # Validate public key using validate_public_key function
        if not validate_public_key(public_key):
            logging.error("Invalid public key format from %s", client_address)
            return "ERROR: Invalid public key format."

        # Add user to the database
        result = self.db_manager.add_user(name, last_name, phone_number, password, public_key)
        if "Error" in result:
            logging.error("Error adding user to the database from %s: %s", client_address, result)
            return result
        else:
            logging.info("User %s %s registered successfully from %s", name, last_name, client_address)
            return f"SUCCESS: User {name} {last_name} registered."