import json
import logging
from Server.Handlers.MessageType import MessageType


class SendMessageHandler:
    def __init__(self, db_manager, clients):
        self.db_manager = db_manager
        self.clients = clients

    def send_response(self, connection, message_type, message):
        response = json.dumps({"type": message_type, "data": message})
        connection.sendall(response.encode('utf-8'))

    def SendBySecureChannel(self, connection, message_type, message):
        # This is not a real secure channel, just a demonstration for the sake of the project
        response = json.dumps({"type": message_type, "data": message})
        connection.sendall(response.encode('utf-8'))


    def send_message(self, sender_phone_number, receiver_phone_number, iv, ciphertext, timestamp, salt):
        receiver_connection = self.clients.get_connected_user(receiver_phone_number)
        message_data = {
            "type": MessageType.INCOMING_CHAT_MESSAGE.value,
            "data": {
                "sender_phone_number": sender_phone_number,
                "iv": iv,
                "ciphertext": ciphertext,
                "timestamp": timestamp,
                "salt": salt
            }
        }
        if receiver_connection:
            receiver_connection.sendall(json.dumps(message_data).encode('utf-8'))
            logging.info("Message sent to %s from %s: iv: %s , ciphertext: %s , salt: %s", receiver_phone_number, sender_phone_number, iv, ciphertext,salt)
        else:
            self.db_manager.add_offline_message(sender_phone_number, receiver_phone_number, iv, ciphertext, timestamp, salt)
            logging.info("User %s is offline. Message saved.", receiver_phone_number)

        sender_connection = self.clients.get_connected_user(sender_phone_number)
        if sender_connection:
            self.send_response(sender_connection, MessageType.OUTGOING_CHAT_MESSAGE_SUCCESS.value, "Message sent successfully")

    def send_offline_messages(self, phone_number):
        offline_messages = self.db_manager.get_offline_messages(phone_number)
        for message in offline_messages:
            sender_phone_number, iv, ciphertext, salt, timestamp = message
            self.send_message(sender_phone_number, phone_number, iv, ciphertext, timestamp, salt)
        self.db_manager.delete_offline_messages(phone_number)
        logging.info("Offline messages sent to %s", phone_number)