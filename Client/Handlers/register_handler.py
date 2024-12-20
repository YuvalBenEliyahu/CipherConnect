import hashlib
import hmac
import json
import logging

from Client.Handlers.message_type import MessageType
from Client.config import ENCODE
from Client.encryption import encrypt_data, load_server_public_key
from Client.queue_manager import message_queue
from Client.utils import get_input, validate_non_empty, validate_phone_number


def register(client_socket, public_key_pem):
    """Register the client with the server."""

    # Request server key for registration
    try:
        client_socket.sendall(json.dumps({
            "type": MessageType.REGISTER_REQUEST_KEY.value,
            "data": {}
        }).encode(ENCODE))

        while True:
            if not message_queue.empty():
                response = message_queue.get()
                if response.get("type") == MessageType.REGISTER_RESPONSE_KEY.value:
                    six_digit_password = response.get("data").get("password")
                    print(f"Received 6-digit password: {six_digit_password}")
                    break
                elif response.get("type") == MessageType.ERROR.value:
                    print(f"Request failed: {response.get('message')}")
                    return
    except Exception as e:
        print(f"Error during registration key request: {e}")
        return

    first_name = get_input("Enter your first name: ", validate_non_empty, "First name cannot be empty.")
    last_name = get_input("Enter your last name: ", validate_non_empty, "Last name cannot be empty.")
    phone_number = get_input("Enter your phone number: ", validate_phone_number, "Phone number must start with '05'.")
    password = get_input("Enter your password: ", validate_non_empty, "Password cannot be empty.")

    signature = hmac.new(six_digit_password.encode(), public_key_pem, hashlib.sha256).hexdigest()

    data = json.dumps({
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "password": password,
        "signature": signature
    })

    try:
        public_key = load_server_public_key()
        encrypted_data = encrypt_data(data, public_key)

        payload = json.dumps({
            "type": MessageType.REGISTER.value,
            "data": {
                "encrypted_data": encrypted_data.hex(),
                "public_key": public_key_pem.decode('utf-8')
            }
        })

        client_socket.sendall(payload.encode(ENCODE))

        while True:
            if not message_queue.empty():
                response = message_queue.get()
                if response.get("type") == MessageType.REGISTRATION_SUCCESS.value:
                    print("Registration successful!")
                    break
                elif response.get("type") == MessageType.ERROR.value:
                    print(f"Registration failed: {response.get('message')}")
                    break
    except Exception as e:
        logging.error(f"An error occurred during registration: {e}")
