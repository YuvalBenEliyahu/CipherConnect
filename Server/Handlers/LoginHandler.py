import json
import logging
from Server.Handlers.SendMessageHandler import SendMessageHandler


class LoginHandler:
    def __init__(self, db_manager, clients):
        self.db_manager = db_manager
        self.clients = clients
        self.message_handler = SendMessageHandler(db_manager, clients)

    def handle_login(self, payload, client_address, connection):
        logging.debug("Handling login with payload: %s from %s", payload, client_address)

        data = self.parse_payload(payload, client_address)
        if not data:
            return "ERROR: Invalid JSON format."

        phone_number = data.get("phone_number")
        password = data.get("password")

        if not self.validate_login_data(phone_number, password, client_address):
            return "ERROR: Missing login data."

        user = self.get_user(phone_number, client_address)
        if not user:
            return "ERROR: User not found."

        if not self.validate_password(user, password, client_address):
            return "ERROR: Incorrect password."

        self.register_connected_user(phone_number, connection)

        return self.send_offline_messages(phone_number)

    def parse_payload(self, payload, client_address):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            logging.error("Invalid JSON format from %s", client_address)
            return None

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
        return self.message_handler.send_offline_messages(phone_number)