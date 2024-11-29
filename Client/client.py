import socket
import sys


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

    public_key = input("Enter your public key (optional): ").strip()

    # Format the registration data
    registration_data = f"REGISTER|{first_name},{last_name},{phone_number},{password}"
    if public_key:
        registration_data += f",{public_key}"

    client_socket.sendall(registration_data.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")


def send_message(client_socket):
    """Send a message to the server."""
    message = input("Enter your message: ")
    client_socket.sendall(f"MESSAGE {message}".encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")


def end_conversation(client_socket):
    """End the conversation and close the connection."""
    client_socket.sendall("END".encode('utf-8'))
    print("Ending conversation. Goodbye!")
    client_socket.close()
    sys.exit(0)


def start_client(host='127.0.0.1', port=65432):
    """Start the client and process CLI commands."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            while True:
                # Display menu
                print("\nOptions:")
                print("1. Register")
                print("2. Send message")
                print("3. End conversation")
                option = input("Choose an option (1/2/3): ")

                if option == "1":
                    register(client_socket)
                elif option == "2":
                    send_message(client_socket)
                elif option == "3":
                    end_conversation(client_socket)
                else:
                    print("Invalid option. Please try again.")
        except ConnectionRefusedError:
            print(f"Could not connect to server at {host}:{port}")
            sys.exit(1)