import json
import logging

from Server.Handlers.MessageHandler import MessageHandler
from Server.Handlers.MessageType import MessageType
from Server.server import send_message_handler


def parse_payload(payload, client_address):
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        logging.error("Invalid JSON format from %s", client_address)
        return None


class LoginHandler(MessageHandler):
    def handle(self, payload, client_address, connection):
        logging.debug("Handling login with payload: %s from %s", payload, client_address)

        data = parse_payload(payload, client_address)
        if not data:
            self.send_response(connection, MessageType.ERROR.value, "Invalid JSON format.")
            return

        phone_number = data.get("phone_number")
        password = data.get("password")

        if not self.validate_login_data(phone_number, password, client_address):
            self.send_response(connection, MessageType.ERROR.value, "Missing login data.")
            return

        user = self.get_user(phone_number, client_address)
        if not user:
            self.send_response(connection, MessageType.ERROR.value, "User not found.")
            return

        if not self.validate_password(user, password, client_address):
            self.send_response(connection, MessageType.ERROR.value, "Incorrect password.")
            return

        self.register_connected_user(phone_number, connection)
        self.send_offline_messages(phone_number)
        self.send_response(connection, MessageType.LOGIN_SUCCESS.value, "Login successful.")

    def validate_login_data(self, phone_number, password, client_address):
        if not phone_number or not password:
            logging.error("Missing login data from %s", client_address)
            return False
        return True

    def get_user(self, phone_number, client_address):
        user = self.db_manager.get_user_by_phone_number(phone_number)
        if not user:
            logging.error("User not found from %s", client_address)
        return user

    def validate_password(self, user, password, client_address):
        if user["password"] != password:
            logging.error("Incorrect password from %s", client_address)
            return False
        return True

    def register_connected_user(self, phone_number, connection):
        self.clients.add_connected_user(phone_number, connection)

    def send_offline_messages(self, phone_number):
        return send_message_handler.send_offline_messages(phone_number)