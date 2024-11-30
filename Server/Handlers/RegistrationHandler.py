import re
import json
import logging

from Server.Handlers.MessageHandler import MessageHandler
from Server.Handlers.MessageType import MessageType
from Server.utils import password_check, validate_public_key


class RegistrationHandler(MessageHandler):

    def handle(self, payload, client_address, connection):
        logging.debug("Handling registration with payload: %s from %s", payload, client_address)
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            self.send_response(connection, MessageType.ERROR, "Invalid JSON format.")
            return

        name = data.get("first_name")
        last_name = data.get("last_name")
        phone_number = data.get("phone_number")
        password = data.get("password")
        public_key = data.get("public_key")

        if not name or not last_name or not phone_number or not password or not public_key:
            self.send_response(connection, MessageType.ERROR.value, "Missing registration data.")
            return

        # Validate name (only letters and spaces)
        if not re.match(r'^[A-Za-z\s]+$', name):
            self.send_response(connection, MessageType.ERROR.value, "Invalid name format.")
            return

        if not re.match(r'^[A-Za-z\s]+$', last_name):
            self.send_response(connection, MessageType.ERROR.value, "Invalid last name format.")
            return

        # Validate phone number (only digits, length 10)
        if not re.match(r'^\d{10}$', phone_number):
            self.send_response(connection, MessageType.ERROR.value, "Invalid phone number format.")
            return

        # Validate password using password_check function
        if not password_check(password):
            self.send_response(connection, MessageType.ERROR.value, "Invalid password format.")
            return

        # Validate public key using validate_public_key function
        if not validate_public_key(public_key):
            self.send_response(connection, MessageType.ERROR.value, "Invalid public key format.")
            return

        # Add user to the database
        result = self.db_manager.add_user(name, last_name, phone_number, password, public_key)
        if "Error" in result:
            self.send_response(connection, MessageType.ERROR.value, result)
        else:
            self.send_response(connection, MessageType.REGISTRATION_SUCCESS.value, f"User {name} {last_name} registered.")