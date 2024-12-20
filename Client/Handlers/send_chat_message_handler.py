import json
from datetime import datetime

from Client.Handlers.key_handler import get_public_key
from Client.Handlers.message_type import MessageType
from Client.config import TIME_STAMP_FORMAT, ENCODE
from Client.encryption import derive_symmetric_key, encrypt_message
from Client.queue_manager import message_queue


def send_chat_message(client_socket, to_phone_number, db_manager, private_key):
    """Send an encrypted message to a specific user."""
    try:
        peer_public_key = get_public_key(client_socket, to_phone_number)
        if not peer_public_key:
            print(f"Public key not found for {to_phone_number}.")
            return
        symmetric_key, salt = derive_symmetric_key(private_key, peer_public_key)

        message = input("Enter your message: ")
        iv, ciphertext = encrypt_message(message, symmetric_key)
        timestamp = datetime.now().strftime(TIME_STAMP_FORMAT)

        data = json.dumps({
            "type": MessageType.OUTGOING_CHAT_MESSAGE.value,
            "data": {
                "receiver_phone_number": to_phone_number,
                "iv": iv.hex(),
                "ciphertext": ciphertext.hex(),
                "timestamp": timestamp,
                "salt": salt.hex()
            }
        })
        client_socket.sendall(data.encode(ENCODE))

        response = message_queue.get(timeout=5)
        if response.get("type") == MessageType.OUTGOING_CHAT_MESSAGE_SUCCESS.value:
            print(f"Message sent to {to_phone_number}!")
            db_manager.add_chat_message(to_phone_number, f"You: {message}", timestamp)
        else:
            print(f"Failed to send message: {response.get('message')}")
    except Exception as e:
        print(f"An error occurred: {e}")