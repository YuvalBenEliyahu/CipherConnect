import json
from Client.Handlers.chat_handler import MessageType
from Client.config import ENCODE
from Client.utils import get_input, validate_non_empty, validate_phone_number

def login(client_socket, message_queue):
    """Login the client with the server."""
    phone_number = get_input("Enter your phone number: ", validate_phone_number, "Phone number must be 10 digits long and start with '05'. Please try again.")
    password = get_input("Enter your password: ", validate_non_empty, "Password cannot be empty. Please try again.")

    data = json.dumps({
        "type": "LOGIN",
        "data": {
            "phone_number": phone_number,
            "password": password
        }
    })

    try:
        client_socket.sendall(data.encode(ENCODE))

        # Wait for login response
        while True:
            if not message_queue.empty():
                response = message_queue.get()
                if response.get("type") == MessageType.LOGIN_SUCCESS.value:
                    print("Login successful!")
                    break
                elif response.get("type") == MessageType.ERROR.value:
                    print(f"Login failed: {response.get('message')}")
                    break
    except ConnectionAbortedError as e:
        print(f"Connection was aborted: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
