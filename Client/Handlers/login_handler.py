import json
from Client.Handlers.message_type import MessageType
from Client.config import ENCODE
from Client.queue_manager import message_queue
from Client.utils import get_input, validate_non_empty, validate_phone_number


def login(client_socket):
    """Login the client with the server."""
    phone_number = get_input("Enter your phone number: ", validate_phone_number,
                             "Phone number must be 10 digits long and start with '05'. Please try again.")
    password = get_input("Enter your password: ", validate_non_empty, "Password cannot be empty. Please try again.")

    data = json.dumps({
        "type": MessageType.LOGIN.value,
        "data": {
            "phone_number": phone_number,
            "password": password
        }
    })

    try:
        client_socket.sendall(data.encode(ENCODE))

        while True:
            if not message_queue.empty():
                response = message_queue.get()
                if response.get("type") == MessageType.LOGIN_SUCCESS.value:
                    print("Login successful!")
                    return True
                elif response.get("type") == MessageType.ERROR.value:
                    return False
    except ConnectionAbortedError as e:
        print(f"Connection was aborted: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
