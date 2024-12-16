import json
import queue

from Client.Handlers.message_type import MessageType
from Client.config import ENCODE
from Client.encryption import serialize_public_key, load_public_key

discovered_keys = {}
public_key_queue = queue.Queue()


def get_public_key(client_socket, phone_number):
    """Retrieve a public key from the cache with retry logic."""
    retries = 3
    for attempt in range(retries):
        print(f"Attempt {attempt + 1}: Checking for public key for {phone_number}.")
        if phone_number not in discovered_keys:
            request_public_key(client_socket, phone_number)

            try:
                # Wait for the public key to be received
                public_key_queue.get(timeout=10)
                if phone_number in discovered_keys:
                    print(f"Public key discovered for {phone_number} on attempt {attempt + 1}.")
                    return discovered_keys.get(phone_number)
            except queue.Empty:
                print(f"Attempt {attempt + 1}: Timeout while waiting for public key for {phone_number}.")

        else:
            return discovered_keys.get(phone_number)

    print(f"Failed to retrieve public key for {phone_number} after {retries} attempts.")
    return None


def send_public_key(client_socket, private_key, peer_phone_number):
    """Send the public key to a peer."""
    try:
        serialized_key = serialize_public_key(private_key.public_key())

        data = json.dumps({
            "type": MessageType.REQUEST_PUBLIC_KEY.value,
            "data": {
                "receiver_phone_number": peer_phone_number,
                "public_key": serialized_key.hex()
            }
        })
        client_socket.sendall(data.encode(ENCODE))
    except Exception as e:
        print(f"An error occurred while sending the public key: {e}")


def request_public_key(client_socket, peer_phone_number):
    """Request a public key from the server for a specific peer."""
    try:
        data = json.dumps({
            "type": MessageType.REQUEST_PUBLIC_KEY.value,
            "data": {
                "peer_phone_number": peer_phone_number
            }
        })
        client_socket.sendall(data.encode(ENCODE))
    except Exception as e:
        print(f"An error occurred while requesting the public key: {e}")


def receive_public_key(received_message):
    """Receive and deserialize the public key from a peer."""
    try:
        message_data = received_message.get("data")
        public_key_pem = message_data.get("public_key").encode()
        peer_phone_number = message_data.get("sender_phone_number")
        peer_public_key = load_public_key(public_key_pem)
        discovered_keys[peer_phone_number] = peer_public_key
        print(f"Discovered public key for {peer_phone_number}.")

        # Notify waiting threads
        public_key_queue.put(peer_phone_number)

        return peer_public_key
    except Exception as e:
        print(f"An error occurred while receiving the public key: {e}")
