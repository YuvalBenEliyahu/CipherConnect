import json
import threading

from Client.config import BUFFER_SIZE, ENCODE
from Client.Database.Database import ClientDatabaseManager

db_manager = ClientDatabaseManager()


def send_message(client_socket, to_phone_number):
    """Send a message to a specific user."""
    message = input("Enter your message: ")
    data = json.dumps({
        "command": "MESSAGE",
        "data": {
            "receiver_phone_number": to_phone_number,
            "message": message
        }
    })
    client_socket.sendall(data.encode(ENCODE))
    response = client_socket.recv(BUFFER_SIZE).decode(ENCODE)
    print(f"Server response: {response}")
    db_manager.add_chat_message(to_phone_number, f"You: {message}")
    print_chat(to_phone_number)


def receive_messages(client_socket):
    """Receive messages from the server."""
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE).decode(ENCODE)
            if not data:
                break

            message_data = json.loads(data)
            sender_phone_number = message_data.get("sender_phone_number")
            message = message_data.get("message")
            if sender_phone_number and message:
                db_manager.add_chat_message(sender_phone_number, f"{sender_phone_number}: {message}")
                print_chat(sender_phone_number)
        except Exception as e:
            print(f"An error occurred while receiving messages: {e}")
            break


def view_chats():
    """View all chats."""
    phone_numbers = db_manager.get_all_phone_numbers_with_chats()
    if not phone_numbers:
        print("No chats available.")
        return
    for phone_number in phone_numbers:
        print(f"Chat with {phone_number}:")
        messages = db_manager.get_chat_messages(phone_number)
        for message, timestamp in messages:
            print(f"  {timestamp} - {message}")
        print()


def navigate_chats(client_socket):
    """Navigate between chats and send messages."""
    while True:
        view_chats()
        print("Options:")
        print("1. Enter phone number to chat")
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
            db_manager.delete_chat(phone_number)
            print(f"Chat with {phone_number} deleted.")
        elif option == '1':
            phone_number = input("Enter phone number to chat: ").strip()
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