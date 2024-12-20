import json
from Client.Handlers.message_type import MessageType
from Client.config import ENCODE
from Client.queue_manager import message_queue
from Client.utils import get_input, validate_non_empty, validate_phone_number
import hmac
import hashlib


def register(client_socket, public_key_pem):
    """Register the client with the server."""

    # Send REGISTER_REQUEST_KEY to the server
    request_data = json.dumps({
        "type": MessageType.REGISTER_REQUEST_KEY.value,
        "data": {}
    })

    try:
        client_socket.sendall(request_data.encode(ENCODE))

        # Wait for REGISTER_RESPONSE_KEY response
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
        print(f"An error occurred: {e}")
        return

    first_name = get_input("Enter your first name: ", validate_non_empty, "First name cannot be empty. Please try again.")
    last_name = get_input("Enter your last name: ", validate_non_empty, "Last name cannot be empty. Please try again.")
    phone_number = get_input("Enter your phone number: ", validate_phone_number, "Phone number must be 10 digits long and start with '05'. Please try again.")
    password = get_input("Enter your password: ", validate_non_empty, "Password cannot be empty. Please try again.")

    # Sign the public key using the 6-digit password
    signature = hmac.new(six_digit_password.encode(), public_key_pem, hashlib.sha256).hexdigest()

    data = json.dumps({
        "type": MessageType.REGISTER.value,
        "data": {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "password": password,
            "public_key": public_key_pem.decode('utf-8'),
            "signature": signature
        }
    })

    try:
        client_socket.sendall(data.encode(ENCODE))

        # Wait for registration response
        while True:
            if not message_queue.empty():
                response = message_queue.get()
                if response.get("type") == MessageType.REGISTRATION_SUCCESS.value:
                    print("Registration successful!")
                    break
                elif response.get("type") == MessageType.ERROR.value:
                    print(f"Registration failed: {response.get('message')}")
                    break
    except ConnectionAbortedError as e:
        print(f"Connection was aborted: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")