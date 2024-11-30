import json
import logging

from datetime import datetime
from Server.Handlers.MessageHandler import MessageHandler
from Server.Handlers.MessageType import MessageType


class SendMessageHandler(MessageHandler):
    def send_message(self, sender_phone_number, receiver_phone_number, message, timestamp):
        receiver_connection = self.clients.get_connected_user(receiver_phone_number)
        message_data = {
            "type": MessageType.MESSAGE.value,
            "data": {
                "sender": sender_phone_number,
                "message": message,
                "timestamp": timestamp
            }
        }
        if receiver_connection:
            # Send message to the connected user
            receiver_connection.sendall(json.dumps(message_data).encode('utf-8'))
            logging.info("Message sent to %s", receiver_phone_number)
            self.send_response(receiver_connection, MessageType.SUCCESS.value, "Message delivered")
        else:
            # Save message as offline
            self.db_manager.add_offline_message(sender_phone_number, receiver_phone_number, message, timestamp)
            logging.info("User %s is offline. Message saved.", receiver_phone_number)
            self.send_response(receiver_connection, MessageType.SUCCESS.value, "User is offline. Message saved")

    def send_offline_messages(self, phone_number):
        offline_messages = self.db_manager.get_offline_messages(phone_number)
        for message in offline_messages:
            self.send_message(message['sender'], phone_number, message['message'], message['timestamp'])
        self.db_manager.delete_offline_messages(phone_number)
        return "SUCCESS: Offline messages sent."