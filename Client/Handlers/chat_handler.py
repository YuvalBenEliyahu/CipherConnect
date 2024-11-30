import json
from datetime import datetime

from Client.config import BUFFER_SIZE, ENCODE
from Client.Database.Database import ClientDatabaseManager

db_manager = ClientDatabaseManager()


def send_message(client_socket, to_phone_number):
    """Send a message to a specific user."""
    try:
        message = input("Enter your message: ")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = json.dumps({
            "type": "MESSAGE",
            "data": {
                "receiver_phone_number": to_phone_number,
                "message": message,
                "timestamp": timestamp
            }
        })
        client_socket.sendall(data.encode(ENCODE))
        response = client_socket.recv(BUFFER_SIZE).decode(ENCODE)
        print(f"Server response: {response}")
        db_manager.add_chat_message(to_phone_number, f"You: {message}", timestamp)
        print_chat(to_phone_number)
    except ConnectionAbortedError as e:
        print(f"Connection was aborted: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def receive_messages(client_socket):
    """Receive messages from the server."""
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE).decode(ENCODE)
            if not data:
                break

            message_data = json.loads(data)
            message_type = message_data.get("type")

            if message_type == "LOGIN_SUCCESS":
                print("Login successful!")
            elif message_type == "REGISTRATION_SUCCESS":
                print("Registration successful!")
            elif message_type == "MESSAGE_SUCCESS":
                sender_phone_number = message_data.get("sender_phone_number")
                message = message_data.get("message")
                timestamp = message_data.get("timestamp")
                if sender_phone_number and message:
                    db_manager.add_chat_message(sender_phone_number, f"{sender_phone_number}: {message}", timestamp)
                    print_chat(sender_phone_number)
            elif message_type == "SUCCESS":
                print(f"Server response: {message_data.get('message')}")
            elif message_type == "ERROR":
                print(f"Server error: {message_data.get('message')}")
            else:
                print(f"Unknown message type: {message_type}")

        except Exception as e:
            print(f"An error occurred while receiving messages: {e}")
            break


def view_chats():
    """View all chats."""
    phone_numbers = db_manager.get_all_phone_numbers_with_chats()
    if not phone_numbers:
        print("No chats available.")
        return []
    print("Available chats:")
    for phone_number in phone_numbers:
        print(f"  {phone_number}")
    return phone_numbers


def navigate_chats(client_socket):
    """Navigate between chats and send messages."""
    while True:
        phone_numbers = view_chats()
        if not phone_numbers:
            break
        print("Options:")
        print("1. Enter phone number to view chat")
        print("2. Enter phone number to delete chat")
        print("3. Delete all chats")
        print("4. Go back")
        option = input("Choose an option (1/2/3/4): ").strip()

        if option == '4':
            break
        elif option == '3':
            db_manager.delete_all_chats()
            print("All chats deleted.")
        elif option == '2':
            phone_number = input("Enter phone number to delete chat: ").strip()
            if phone_number in phone_numbers:
                db_manager.delete_chat(phone_number)
                print(f"Chat with {phone_number} deleted.")
            else:
                print("Invalid phone number. Please try again.")
        elif option == '1':
            phone_number = input("Enter phone number to view chat: ").strip()
            print_chat(phone_number)
            send_message(client_socket, phone_number)
        else:
            print("Invalid option. Please try again.")

def print_chat(phone_number):
    """Print the chat with a specific user."""
    messages = db_manager.get_chat_messages(phone_number)
    if messages:
        print(f"Chat with {phone_number}:")
        for message, timestamp in messages:
            print(f"  {timestamp} - {message}")
    else:
        print("No chat history with this number.")

