import json


class MessageHandler:
    def __init__(self, db_manager, clients):
        self.db_manager = db_manager
        self.clients = clients

    def send_response(self, connection, message_type, message):
        response = json.dumps({"type": message_type, "message": message})
        connection.sendall(response.encode('utf-8'))

    def handle(self, payload, client_address, connection):
        raise NotImplementedError("Subclasses should implement this method.")