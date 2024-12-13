import json
from Client.Handlers.chat_handler import db_manager, print_chat
from Client.Handlers.message_type import MessageType
from Client.config import BUFFER_SIZE, ENCODE
from Client.Handlers.receive_chat_message_handler import receive_chat_message


def receive_server_messages(client_socket, message_queue):
    """Receive messages from the server and enqueue them."""
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE).decode(ENCODE)
            if not data:
                print("Server closed the connection.")
                break

            if data.strip():  # Check if data is not empty
                message_data = json.loads(data)
                message_type = message_data.get("type")

                if message_type == MessageType.LOGIN_SUCCESS.value:
                    message_queue.put(message_data)
                elif message_type == MessageType.REGISTRATION_SUCCESS.value:
                    message_queue.put(message_data)
                elif message_type == MessageType.OUTGOING_MESSAGE_SUCCESS.value:
                    sender_phone_number = message_data.get("sender_phone_number")
                    message = message_data.get("message")
                    timestamp = message_data.get("timestamp")
                    if sender_phone_number and message:
                        db_manager.add_chat_message(sender_phone_number, f"{sender_phone_number}: {message}", timestamp)
                        print_chat(sender_phone_number)
                elif message_type == MessageType.INCOMING_MESSAGE.value:
                    receive_chat_message(client_socket, message_queue)
                elif message_type == MessageType.SUCCESS.value:
                    print(f"Server response: {message_data.get('message')}")
                elif message_type == MessageType.ERROR.value:
                    print(f"Server error: {message_data.get('message')}")
                    message_queue.put(message_data)
                else:
                    print(f"Unknown message type: {message_type}")
            else:
                print("Received empty data from server.")
        except Exception as e:
            print(f"An error occurred while receiving messages: {e}")
            break