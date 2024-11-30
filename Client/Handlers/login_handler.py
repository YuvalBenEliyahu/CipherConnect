import json
from Client.config import BUFFER_SIZE, ENCODE
from Client.utils import get_input, validate_non_empty, validate_phone_number


def login(client_socket):
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
        response = client_socket.recv(BUFFER_SIZE).decode(ENCODE)
        return response == "Login successful"
    except ConnectionAbortedError as e:
        print(f"Connection was aborted: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

