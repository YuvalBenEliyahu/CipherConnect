import json
from Client.Handlers.chat_handler import MessageType
from Client.config import ENCODE
from Client.encryption import public_key_pem
from Client.utils import get_input, validate_non_empty, validate_phone_number


def register(client_socket, message_queue):
    """Register the client with the server."""
    first_name = get_input("Enter your first name: ", validate_non_empty, "First name cannot be empty. Please try again.")
    last_name = get_input("Enter your last name: ", validate_non_empty, "Last name cannot be empty. Please try again.")
    phone_number = get_input("Enter your phone number: ", validate_phone_number, "Phone number must be 10 digits long and start with '05'. Please try again.")
    password = get_input("Enter your password: ", validate_non_empty, "Password cannot be empty. Please try again.")

    data = json.dumps({
        "type": "REGISTER",
        "data": {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "password": password,
            "public_key": public_key_pem.decode('utf-8')
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
