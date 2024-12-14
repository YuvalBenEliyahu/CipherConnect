import json
from Client.Handlers.chat_handler import print_chat
from Client.Handlers.key_handler import receive_public_key
from Client.Handlers.message_type import MessageType
from Client.config import BUFFER_SIZE, ENCODE
from Client.Handlers.receive_chat_message_handler import receive_chat_message
from Client.queue_manager import message_queue


def receive_server_messages(client_socket, db_manager, private_key=None):
    """Receive messages from the server and process them."""
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE).decode(ENCODE)
            if not data:
                print("Server closed the connection.")
                break

            if data.strip():
                message_data = json.loads(data)
                message_type = message_data.get("type")

                if message_type == MessageType.LOGIN_SUCCESS.value:
                    message_queue.put(message_data)
                elif message_type == MessageType.REGISTRATION_SUCCESS.value:
                    message_queue.put(message_data)
                elif message_type == MessageType.PUBLIC_KEY_SUCCESS.value:
                    receive_public_key(message_data)
                elif message_type == MessageType.INCOMING_CHAT_MESSAGE.value:
                    receive_chat_message(message_data, db_manager, private_key, client_socket)
                elif message_type == MessageType.OUTGOING_CHAT_MESSAGE_SUCCESS.value:
                    message_queue.put(message_data)
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
