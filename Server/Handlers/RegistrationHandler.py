import re
import logging
import hmac
import hashlib
from Server.Handlers.MessageType import MessageType
from Server.utils import password_check, validate_public_key, derive_key


class RegistrationHandler:
    def __init__(self, db_manager, clients, send_message_handler, pending_registrations):
        self.db_manager = db_manager
        self.clients = clients
        self.send_message_handler = send_message_handler
        self.pending_registrations = pending_registrations

    def handle(self, data, client_address, connection):
        logging.debug("Handling registration with data: %s from %s", data, client_address)

        name = data.get("first_name")
        last_name = data.get("last_name")
        phone_number = data.get("phone_number")
        password = data.get("password")
        public_key = data.get("public_key")
        signature = data.get("signature")

        if not name or not last_name or not phone_number or not password or not public_key or not signature:
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Missing registration data.")
            return

        # Validate name (only letters and spaces)
        if not re.match(r'^[A-Za-z\s]+$', name):
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Invalid name format.")
            return

        if not re.match(r'^[A-Za-z\s]+$', last_name):
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Invalid last name format.")
            return

        # Validate phone number (only digits, length 10)
        if not re.match(r'^\d{10}$', phone_number):
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Invalid phone number format.")
            return

        # Validate password using password_check function
        if not password_check(password):
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Invalid password format.")
            return

        # Validate public key using validate_public_key function
        if not validate_public_key(public_key):
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Invalid public key format.")
            return

        # Check if the six_digit_password is still valid
        six_digit_password = self.pending_registrations.get(client_address)
        if not six_digit_password:
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Password expired or invalid.")
            return

        # Derive key from password
        derived_key, salt = derive_key(password)

        # Verify the signature
        expected_signature = hmac.new(six_digit_password.encode(), public_key.encode(), hashlib.sha256).hexdigest()
        if signature != expected_signature:
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Invalid signature.")
            return

        # Add user to the database
        result = self.db_manager.add_user(name, last_name, phone_number, derived_key, public_key, salt)
        if "Error" in result:
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, result)
        else:
            self.send_message_handler.send_response(connection, MessageType.REGISTRATION_SUCCESS.value, f"User {name} {last_name} registered.")