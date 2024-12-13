import json

from Server.Handlers.LoginHandler import LoginHandler
from Server.Handlers.MessageType import MessageType
from Server.Handlers.ReceiveMessageHandler import ReceiveMessageHandler
from Server.Handlers.RegistrationHandler import RegistrationHandler
from Server.Handlers.SendMessageHandler import SendMessageHandler

class MessageHandler:
    def __init__(self, db_manager, clients):
        self.db_manager = db_manager
        self.clients = clients
        self.send_message_handler = SendMessageHandler(db_manager, clients)

    def validate_request(self, request, connection):
        type = request.get("type")
        payload = request.get("data")

        if not type or not payload:
            connection.send("ERROR: Missing type or payload.".encode())
            return None, None

        return type, payload

    def handle_message(self, request, client_socket, client_address):
        type, payload = self.validate_request(request, client_socket)
        if not type or not payload:
            return

        if type == MessageType.REGISTER.value:
            registration_handler = RegistrationHandler(self.db_manager, self.clients, self.send_message_handler)
            registration_handler.handle(payload, client_address, client_socket)
        elif type == MessageType.LOGIN.value:
            login_handler = LoginHandler(self.db_manager, self.clients, self.send_message_handler)
            login_handler.handle(payload, client_address, client_socket)
        elif type == MessageType.OUTGOING_CHAT_MESSAGE.value:
            receive_message_handler = ReceiveMessageHandler(self.db_manager, self.clients, self.send_message_handler)
            receive_message_handler.handle(payload, client_address, client_socket)
        else:
            self.send_message_handler.send_response(client_socket, MessageType.ERROR.value, f"Unknown type '{type}'")