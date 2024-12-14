from Client.Handlers.send_chat_message_handler import send_chat_message


def view_chats(db_manager):
    """View all chats."""
    phone_numbers = db_manager.get_all_phone_numbers_with_chats()
    if not phone_numbers:
        return []
    print("Available chats:")
    for phone_number in phone_numbers:
        print(f"  {phone_number}")
    return phone_numbers


def navigate_chats(client_socket, db_manager, private_key):
    """Navigate between chats and send messages."""
    while True:
        phone_numbers = view_chats(db_manager)
        if not phone_numbers:
            print("No chats available.")
            print("Options:")
            print("1. Start a new chat")
            print("2. Go back")
            option = input("Choose an option (1/2): ").strip()

            if option == '2':
                break
            elif option == '1':
                phone_number = input("Enter phone number to start a new chat: ").strip()
                send_chat_message(client_socket, phone_number, db_manager, private_key)
            else:
                print("Invalid option. Please try again.")
        else:
            print("Options:")
            print("1. Enter phone number to view chat")
            print("2. Enter phone number to delete chat")
            print("3. Delete all chats")
            print("4. Start a new chat")
            print("5. Go back")
            option = input("Choose an option (1/2/3/4/5): ").strip()

            if option == '5':
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
                print_chat(phone_number, db_manager)
                send_chat_message(client_socket, phone_number, db_manager, private_key)
            elif option == '4':
                phone_number = input("Enter phone number to start a new chat: ").strip()
                send_chat_message(client_socket, phone_number, db_manager, private_key)
            else:
                print("Invalid option. Please try again.")


def print_chat(phone_number, db_manager):
    """Print the chat with a specific user."""
    messages = db_manager.get_chat_messages(phone_number)
    if messages:
        print(f"Chat with {phone_number}:")
        for message, timestamp in messages:
            print(f"  {timestamp} - {message}")
    else:
        print("No chat history with this number.")
