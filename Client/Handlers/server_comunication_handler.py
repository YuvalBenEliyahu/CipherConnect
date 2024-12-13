import json
from Client.Handlers.chat_handler import MessageType, db_manager, print_chat
from Client.config import BUFFER_SIZE, ENCODE

def receive_server_messages(client_socket, message_queue):
    """Receive messages from the server and enqueue them."""
    while True:
        try:
            # Receive raw data from the server
            data = client_socket.recv(BUFFER_SIZE).decode(ENCODE)
            if not data:
                print("Server closed the connection.")
                break  # Stop if connection is closed

            # Parse the message
            message_data = json.loads(data)
            message_type = message_data.get("type")

            # Handle specific message types
            if message_type == MessageType.LOGIN_SUCCESS.value:
                message_queue.put(message_data)  # Notify the main thread
            elif message_type == MessageType.REGISTRATION_SUCCESS.value:
                message_queue.put(message_data)
            elif message_type == MessageType.MESSAGE_SUCCESS.value:
                sender_phone_number = message_data.get("sender_phone_number")
                message = message_data.get("message")
                timestamp = message_data.get("timestamp")
                if sender_phone_number and message:
                    db_manager.add_chat_message(sender_phone_number, f"{sender_phone_number}: {message}", timestamp)
                    print_chat(sender_phone_number)
            elif message_type == MessageType.SUCCESS.value:
                print(f"Server response: {message_data.get('message')}")
            elif message_type == MessageType.ERROR.value:
                print(f"Server error: {message_data.get('message')}")
                message_queue.put(message_data)  # Notify the main thread
            else:
                print(f"Unknown message type: {message_type}")
        except Exception as e:
            print(f"An error occurred while receiving messages: {e}")
            break
