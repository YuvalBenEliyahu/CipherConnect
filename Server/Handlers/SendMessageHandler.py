import json
import logging
from datetime import datetime

class SendMessageHandler:
    def __init__(self, db_manager, clients):
        self.db_manager = db_manager
        self.clients = clients

    def send_message(self, sender_phone_number, receiver_phone_number, message):
        receiver_connection = self.clients.get_connected_user(receiver_phone_number)
        if receiver_connection:
            # Send message to the connected user
            message_data = json.dumps({
                "command": "MESSAGE",
                "data": {
                    "sender": sender_phone_number,
                    "message": message,
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            })
            receiver_connection.sendall(message_data.encode('utf-8'))
            logging.info("Message sent to %s", receiver_phone_number)
            return json.dumps({"status": "SUCCESS", "message": "Message delivered"})
        else:
            # Save message as offline
            self.db_manager.add_offline_message(sender_phone_number, receiver_phone_number, message)
            logging.info("User %s is offline. Message saved.", receiver_phone_number)
            return json.dumps({"status": "SUCCESS", "message": "User is offline. Message saved."})

    def send_offline_messages(self, phone_number):
        offline_messages = self.db_manager.get_offline_messages(phone_number)
        for message in offline_messages:
            self.send_message(message['sender'], phone_number, message['message'])
        self.db_manager.delete_offline_messages(phone_number)
        return "SUCCESS: Offline messages sent."