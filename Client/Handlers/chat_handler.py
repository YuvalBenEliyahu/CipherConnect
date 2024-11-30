from Client.config import BUFFER_SIZE
from Client.Data.chat_data import chats


def send_message(client_socket, phone_number):
    """Send a message to a specific user."""
    message = input("Enter your message: ")
    client_socket.sendall(f"MESSAGE {phone_number} {message}".encode('utf-8'))
    response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    print(f"Server response: {response}")
    if phone_number in chats:
        chats[phone_number].append(f"You: {message}")
    else:
        chats[phone_number] = [f"You: {message}"]
    print_chat(phone_number)


def view_chats():
    """View all chats."""
    if not chats:
        print("No chats available.")
        return
    for phone_number, messages in chats.items():
        print(f"Chat with {phone_number}:")
        for message in messages:
            print(f"  {message}")
        print()


def navigate_chats(client_socket):
    """Navigate between chats and send messages."""
    while True:
        view_chats()
        phone_number = input("Enter the phone number to chat with (or 'exit' to go back): ").strip()
        if phone_number.lower() == 'exit':
            break
        if phone_number not in chats:
            print("No chat history with this number. Starting a new chat.")
            chats[phone_number] = []
        send_message(client_socket, phone_number)


def print_chat(phone_number):
    """Print the chat with a specific user."""
    if phone_number in chats:
        print(f"Chat with {phone_number}:")
        for message in chats[phone_number]:
            print(f"  {message}")
    else:
        print("No chat history with this number.")

