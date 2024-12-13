import json
from Client.Handlers.message_type import MessageType
from Client.Database.Database import ClientDatabaseManager

db_manager = ClientDatabaseManager()


def receive_chat_message(client_socket, message_queue):
    """Receive a chat message from the server."""
    try:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            print("Server closed the connection.")

        message_data = json.loads(data)
        message_type = message_data.get("type")

        if message_type == MessageType.INCOMING_CHAT_MESSAGE.value:
            sender_phone_number = message_data.get("sender_phone_number")
            message = message_data.get("message")
            timestamp = message_data.get("timestamp")
            if sender_phone_number and message:
                db_manager.add_chat_message(sender_phone_number, f"{sender_phone_number}: {message}", timestamp)
                print(f"New message from {sender_phone_number}: {message}")
        else:
            message_queue.put(message_data)
    except Exception as e:
        print(f"An error occurred while receiving messages: {e}")
