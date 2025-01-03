import random
import threading

from Server.Handlers.LoginHandler import LoginHandler
from Server.Handlers.MessageType import MessageType
from Server.Handlers.ReceiveMessageHandler import ReceiveMessageHandler
from Server.Handlers.RegistrationHandler import RegistrationHandler
from Server.Handlers.SendMessageHandler import SendMessageHandler
from Server.Handlers.keyHandler import KeyHandler


class MessageHandler:
    def __init__(self, db_manager, clients):
        self.db_manager = db_manager
        self.clients = clients
        self.send_message_handler = SendMessageHandler(db_manager, clients)
        self.pending_registrations = {}

    def validate_request(self, request, connection):
        type = request.get("type")

        if not type:
            connection.send("ERROR: Missing type.".encode())
            return None

        return type

    def handle_message(self, request, client_socket, client_address):
        type = self.validate_request(request, client_socket)
        if not type:
            return

        print(f"Received message of type: {type} from {client_address}")

        handler = self.get_handler(type)
        if handler:
            handler(request.get("data"), client_socket, client_address)
        else:
            print(f"Unknown message type: {type} from {client_address}")
            self.send_message_handler.send_response(client_socket, MessageType.ERROR.value, f"Unknown type '{type}'")

    def get_handler(self, type):
        return {
            MessageType.REGISTER_REQUEST_KEY.value: self.handle_register_request_key,
            MessageType.REGISTER.value: self.handle_register,
            MessageType.LOGIN.value: self.handle_login,
            MessageType.OUTGOING_CHAT_MESSAGE.value: self.handle_outgoing_chat_message,
            MessageType.REQUEST_PUBLIC_KEY.value: self.handle_request_public_key,
        }.get(type)

    def handle_register_request_key(self, payload, client_socket, client_address):
        print(f"Handling register request key for {client_address}")
        six_digit_password = ''.join(random.choices('0123456789', k=6))
        print(f"Generated 6-digit password: {six_digit_password}")
        self.pending_registrations[client_address] = six_digit_password

        timer = threading.Timer(60.0, self.invalidate_password, [client_address])
        timer.start()

        self.send_message_handler.SendBySecureChannel(client_socket, MessageType.REGISTER_RESPONSE_KEY.value,
                                                      {"password": six_digit_password})

    def handle_register(self, payload, client_socket, client_address):
        print(f"Handling registration for {client_address}")
        registration_handler = RegistrationHandler(self.db_manager, self.clients, self.send_message_handler,
                                                   self.pending_registrations)
        registration_handler.handle(payload, client_address, client_socket)

    def handle_login(self, payload, client_socket, client_address):
        print(f"Handling login for {client_address}")
        login_handler = LoginHandler(self.db_manager, self.clients, self.send_message_handler)
        login_handler.handle(payload, client_address, client_socket)

    def handle_outgoing_chat_message(self, payload, client_socket, client_address):
        print(f"Handling outgoing chat message for {client_address}")
        receive_message_handler = ReceiveMessageHandler(self.db_manager, self.clients, self.send_message_handler)
        receive_message_handler.handle(payload, client_address, client_socket)

    def handle_request_public_key(self, payload, client_socket, client_address):
        print(f"Handling public key request for {client_address}")
        request_public_key_handler = KeyHandler(self.db_manager, self.clients, self.send_message_handler)
        request_public_key_handler.handle(payload, client_address, client_socket)

    def invalidate_password(self, client_address):
        if client_address in self.pending_registrations:
            print(f"Invalidating password for {client_address}")
            del self.pending_registrations[client_address]
