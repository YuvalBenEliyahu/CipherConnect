import json
from Client.config import BUFFER_SIZE, ENCODE
from Client.encryption import public_key_pem
from Client.utils import get_input, validate_non_empty, validate_phone_number


def register(client_socket):
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
        response = client_socket.recv(BUFFER_SIZE).decode(ENCODE)
        print(f"Server response: {response}")
    except ConnectionAbortedError as e:
        print(f"Connection was aborted: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

