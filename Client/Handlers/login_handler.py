import json
from Client.config import BUFFER_SIZE, ENCODE


def login(client_socket):
    """Login the client with the server."""
    while True:
        phone_number = input("Enter your phone number: ").strip()
        if phone_number.isdigit():
            break
        print("Phone number must be numeric. Please try again.")

    while True:
        password = input("Enter your password: ").strip()
        if password:
            break
        print("Password cannot be empty. Please try again.")

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
        print(f"Server response: {response}")
        return response == "Login successful"
    except ConnectionAbortedError as e:
        print(f"Connection was aborted: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

