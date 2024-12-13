import json
import queue
from datetime import datetime
from enum import Enum

from Client.config import BUFFER_SIZE, ENCODE, TIME_STAMP_FORMAT
from Client.Database.Database import ClientDatabaseManager

db_manager = ClientDatabaseManager()


class MessageType(Enum):
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    REGISTRATION_SUCCESS = "REGISTRATION_SUCCESS"
    MESSAGE_SUCCESS = "MESSAGE_SUCCESS"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


def send_chat_message(client_socket, to_phone_number, message_queue):
    """Send a message to a specific user."""
    try:
        message = input("Enter your message: ")
        timestamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        data = json.dumps({
            "type": "MESSAGE",
            "data": {
                "receiver_phone_number": to_phone_number,
                "message": message,
                "timestamp": timestamp
            }
        })
        client_socket.sendall(data.encode(ENCODE))

        # Wait for server response
        try:
            response = message_queue.get(timeout=5)
            if response.get("type") == MessageType.MESSAGE_SUCCESS.value:
                print(f"Message sent to {to_phone_number}!")
                db_manager.add_chat_message(to_phone_number, f"You: {message}", timestamp)
            elif response.get("type") == MessageType.ERROR.value:
                print(f"Failed to send message: {response.get('message')}")
        except queue.Empty:
            print("No response from server. Please try again later.")
    except ConnectionAbortedError as e:
        print(f"Connection was aborted: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


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


def navigate_chats(client_socket, message_queue):
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
            send_chat_message(client_socket, phone_number, message_queue)
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

