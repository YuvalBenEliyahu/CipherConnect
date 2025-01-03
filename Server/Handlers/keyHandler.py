import logging

from cryptography.hazmat.primitives.serialization import load_pem_private_key

from Server.Handlers.MessageType import MessageType
from Server.config import SERVER_PRIVATE_KEY_PATH
from Server.encryption import sign_data


class KeyHandler:
    def __init__(self, db_manager, clients, send_message_handler):
        self.db_manager = db_manager
        self.clients = clients
        self.send_message_handler = send_message_handler
        self.private_key = self.load_private_key(SERVER_PRIVATE_KEY_PATH)

    def load_private_key(self, private_key_path):
        with open(private_key_path, "rb") as key_file:
            private_key = load_pem_private_key(key_file.read(), password=None)
        return private_key

    def handle(self, payload, client_address, connection):
        try:
            peer_phone_number = payload.get("peer_phone_number")
            if not peer_phone_number:
                self.send_message_handler.send_response(connection, MessageType.ERROR.value,
                                                        "Missing peer phone number.")
                return

            logging.info(f"Retrieving public key for peer phone number: {peer_phone_number}")
            public_key = self.db_manager.get_public_key(peer_phone_number)
            if not public_key:
                logging.warning(f"Public key not found for peer phone number: {peer_phone_number}")
                self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Public key not found.")
                return

            # Sign the public key
            signature = sign_data(public_key.encode(), self.private_key)

            response_data = {
                "sender_phone_number": peer_phone_number,
                "public_key": public_key,
                "signature": signature.hex()
            }
            self.send_message_handler.send_response(connection, MessageType.PUBLIC_KEY_SUCCESS.value, response_data)
        except Exception as e:
            logging.error(f"Exception occurred while handling request: {e}")
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, str(e))
