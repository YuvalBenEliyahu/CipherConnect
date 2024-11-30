
import logging

class ReceiveMessage:
    def __init__(self, clients, send_message_handler):
        self.clients = clients
        self.send_message_handler = send_message_handler

    def handle_message(self, connection, payload):
        try:
            sender_phone_number = self.get_phone_number_from_connection(connection)
            receiver_phone_number = payload.get("receiver_phone_number")
            message = payload.get("message")

            if not receiver_phone_number or not message:
                logging.error("Invalid message format.")
                return "ERROR: Invalid message format."

            self.forward_message(sender_phone_number, receiver_phone_number, message)
            return "SUCCESS: Message processed."
        except Exception as e:
            logging.error(f"Exception: {e}")
            return f"ERROR: {str(e)}"

    def get_phone_number_from_connection(self, connection):
        phone_number = self.clients.get_phone_number_by_connection(connection)
        if phone_number:
            return phone_number
        logging.error("Phone number not found for the given connection.")
        return None

    def forward_message(self, sender_phone_number, receiver_phone_number, message):
        response = self.send_message_handler.send_message(sender_phone_number, receiver_phone_number, message)
        logging.info("Forwarded message from %s to %s: %s", sender_phone_number, receiver_phone_number, response)