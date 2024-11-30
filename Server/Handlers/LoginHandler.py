import logging
from Server.Handlers.MessageType import MessageType

class LoginHandler:
    def __init__(self, db_manager, clients, send_message_handler):
        self.db_manager = db_manager
        self.clients = clients
        self.send_message_handler = send_message_handler

    def handle(self, data, client_address, connection):
        logging.debug("Handling login with data: %s from %s", data, client_address)

        try:
            phone_number = data.get("phone_number")
            password = data.get("password")

            if not self.validate_login_data(phone_number, password, client_address):
                self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Missing login data.")
                return

            user = self.get_user(phone_number, client_address)
            if not user:
                self.send_message_handler.send_response(connection, MessageType.ERROR.value, "User not found.")
                return

            if not self.validate_password(user, password, client_address):
                self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Incorrect password.")
                return

            self.register_connected_user(phone_number, connection)
            self.send_offline_messages(phone_number)
            self.send_message_handler.send_response(connection, MessageType.LOGIN_SUCCESS.value, "Login successful.")
        except Exception as e:
            logging.error(f"Exception during login handling: {e}")
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Internal server error.")
        finally:
            logging.debug("Closing connection for client: %s", client_address)
            connection.close()

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
        return self.send_message_handler.send_offline_messages(phone_number)