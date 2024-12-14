import json
from Client.Handlers.message_type import MessageType
from Client.queue_manager import message_queue


def receive_chat_message(received_message, db_manager):
    """Receive a chat message from the server."""
    try:
        message_type = received_message.get("type")
        message_data = received_message.get("data")

        if message_type == MessageType.INCOMING_CHAT_MESSAGE.value:
            sender_phone_number = message_data.get("sender_phone_number")
            message = message_data.get("message")
            timestamp = message_data.get("timestamp")
            if sender_phone_number and message:
                db_manager.add_chat_message(sender_phone_number, f"{sender_phone_number}: {message}", timestamp)
                print(f"New message from {sender_phone_number}: {message}")
        else:
            message_queue.put(received_message)
    except Exception as e:
        print(f"An error occurred while receiving messages: {e}")
