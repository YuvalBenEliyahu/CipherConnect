from datetime import time

from Client.Handlers.key_handler import discovered_keys, request_public_key, get_public_key
from Client.Handlers.message_type import MessageType
from Client.encryption import derive_symmetric_key, decrypt_message
from Client.queue_manager import message_queue


def receive_chat_message(received_message, db_manager, private_key, client_socket):
    """Receive and decrypt a chat message from the server."""
    try:
        message_type = received_message.get("type")
        message_data = received_message.get("data")

        if message_type == MessageType.INCOMING_CHAT_MESSAGE.value:
            sender_phone_number = message_data.get("sender_phone_number")

            peer_public_key = get_public_key(client_socket, sender_phone_number)
            if not peer_public_key:
                print(f"Public key not found for {sender_phone_number}.")
                return
            symmetric_key = derive_symmetric_key(private_key, peer_public_key)

            iv = bytes.fromhex(message_data.get("iv"))
            ciphertext = bytes.fromhex(message_data.get("ciphertext"))
            plaintext = decrypt_message(iv, ciphertext, symmetric_key)

            timestamp = message_data.get("timestamp")
            db_manager.add_chat_message(sender_phone_number, f"{sender_phone_number}: {plaintext}", timestamp)
            print(f"New message from {sender_phone_number}: {plaintext}")
        else:
            message_queue.put(received_message)
    except Exception as e:
        print(f"An error occurred while receiving messages: {e}")
