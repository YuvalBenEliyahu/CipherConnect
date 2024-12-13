import json
import logging
from Server.Handlers.MessageType import MessageType

class SendMessageHandler:
    def __init__(self, db_manager, clients):
        self.db_manager = db_manager
        self.clients = clients

    def send_response(self, connection, message_type, message):
        response = json.dumps({"type": message_type, "message": message})
        connection.sendall(response.encode('utf-8'))

    def send_message(self, sender_phone_number, receiver_phone_number, message, timestamp):
        receiver_connection = self.clients.get_connected_user(receiver_phone_number)
        message_data = {
            "type": MessageType.INCOMING_CHAT_MESSAGE.value,
            "data": {
                "sender": sender_phone_number,
                "message": message,
                "timestamp": timestamp
            }
        }
        if receiver_connection:
            # Send message to the connected user
            receiver_connection.sendall(json.dumps(message_data).encode('utf-8'))
            logging.info("Message sent to %s from %s: %s", receiver_phone_number, sender_phone_number, message)
            self.send_response(receiver_connection, MessageType.SUCCESS.value, "Message delivered")
        else:
            # Save message as offline
            self.db_manager.add_offline_message(sender_phone_number, receiver_phone_number, message, timestamp)
            logging.info("User %s is offline. Message saved.", receiver_phone_number)
            self.send_response(receiver_connection, MessageType.SUCCESS.value, "User is offline. Message saved")

        # Send OUTGOING_CHAT_MESSAGE_SUCCESS to the sender
        sender_connection = self.clients.get_connected_user(sender_phone_number)
        if sender_connection:
            self.send_response(sender_connection, MessageType.OUTGOING_CHAT_MESSAGE_SUCCESS.value, "Message sent successfully")

    def send_offline_messages(self, phone_number):
        offline_messages = self.db_manager.get_offline_messages(phone_number)
        for message in offline_messages:
            self.send_message(message['sender'], phone_number, message['message'], message['timestamp'])
        self.db_manager.delete_offline_messages(phone_number)
        return "SUCCESS: Offline messages sent."