import logging
from Server.Handlers.MessageType import MessageType

class ReceiveMessageHandler:
    def __init__(self, db_manager, clients, send_message_handler):
        self.db_manager = db_manager
        self.clients = clients
        self.send_message_handler = send_message_handler

    def handle(self, payload, client_address, connection):
        try:
            sender_phone_number = self.get_phone_number_from_connection(connection)
            receiver_phone_number = payload.get("receiver_phone_number")
            message = payload.get("message")
            timestamp = payload.get("timestamp")

            if not receiver_phone_number or not message or not timestamp:
                self.send_message_handler.send_response(connection, MessageType.ERROR.value, "Invalid message format.")
                return

            logging.info("Received message from %s to %s: %s", sender_phone_number, receiver_phone_number, message)
            self.forward_message(sender_phone_number, receiver_phone_number, message, timestamp)
            self.send_message_handler.send_response(connection, MessageType.OUTGOING_CHAT_MESSAGE_SUCCESS.value, "Message processed.")
        except Exception as e:
            logging.error(f"Exception: {e}")
            self.send_message_handler.send_response(connection, MessageType.ERROR.value, str(e))

    def get_phone_number_from_connection(self, connection):
        phone_number = self.clients.get_phone_number_by_connection(connection)
        if phone_number:
            return phone_number
        logging.error("Phone number not found for the given connection.")
        return None

    def forward_message(self, sender_phone_number, receiver_phone_number, message, timestamp):
        self.send_message_handler.send_message(sender_phone_number, receiver_phone_number, message, timestamp)