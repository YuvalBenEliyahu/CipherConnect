import logging
from Server.Handlers.MessageType import MessageType


class KeyHandler:
    def __init__(self, db_manager, clients, send_message_handler):
        self.db_manager = db_manager
        self.clients = clients
        self.send_message_handler = send_message_handler

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

            response_data = {
                "sender_phone_number": peer_phone_number,
                "public_key": public_key
            }
            self.send_message_handler.send_response(connection, MessageType.PUBLIC_KEY_SUCCESS.value, response_data)
        except Exception as e:
            logging.error(f"Exception occurred while handling request: {e}")
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, str(e))
