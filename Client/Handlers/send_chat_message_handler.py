import json
import queue
from datetime import datetime

from Client.Handlers.message_type import MessageType
from Client.config import TIME_STAMP_FORMAT, ENCODE
from Server.server import db_manager


def send_chat_message(client_socket, to_phone_number, message_queue):
    """Send a message to a specific user."""
    try:
        message = input("Enter your message: ")
        timestamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        data = json.dumps({
            "type": MessageType.OUTGOING_CHAT_MESSAGE.value,
            "data": {
                "receiver_phone_number": to_phone_number,
                "message": message,
                "timestamp": timestamp
            }
        })
        client_socket.sendall(data.encode(ENCODE))

        # Wait for server response
        try:
            response = message_queue.get(timeout=5)
            if response.get("type") == MessageType.OUTGOING_CHAT_MESSAGE_SUCCESS.value:
                print(f"Message sent to {to_phone_number}!")
                db_manager.add_chat_message(to_phone_number, f"You: {message}", timestamp)
            elif response.get("type") == MessageType.ERROR.value:
                print(f"Failed to send message: {response.get('message')}")
        except queue.Empty:
            print("No response from server. Please try again later.")
    except ConnectionAbortedError as e:
        print(f"Connection was aborted: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")