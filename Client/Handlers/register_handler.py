import json

from Client.config import BUFFER_SIZE


def register(client_socket):
    """Register the client with the server."""
    while True:
        first_name = input("Enter your first name: ").strip()
        if first_name:
            break
        print("First name cannot be empty. Please try again.")

    while True:
        last_name = input("Enter your last name: ").strip()
        if last_name:
            break
        print("Last name cannot be empty. Please try again.")

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
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "password": password
    })
    client_socket.sendall(data.encode('utf-8'))
    response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    print(f"Server response: {response}")