class Clients:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.clients = {}  # In-memory cache for clients
        self.connected_users = {}  # Track connected users

    def add_client(self, name, last_name, phone_number, password, public_key):
        if self.db_manager.add_user(name, last_name, phone_number, password, public_key):
            self.clients[phone_number] = {
                "name": name,
                "last_name": last_name,
                "phone_number": phone_number,
                "public_key": public_key
            }
            return True
        return False

    def get_client(self, phone_number):
        # Check in-memory cache first
        if phone_number in self.clients:
            return self.clients[phone_number]

        # If not in cache, check in database
        user = self.db_manager.get_user_by_phone_number(phone_number)
        if user:
            self.clients[phone_number] = user
            return user
        return None

    def add_connected_user(self, phone_number, connection):
        self.connected_users[phone_number] = connection
        # Load connected user to cache
        user = self.get_client(phone_number)
        if user:
            self.clients[phone_number] = user

    def remove_connected_user(self, phone_number):
        if phone_number in self.connected_users:
            del self.connected_users[phone_number]
        # Remove disconnected user from cache
        if phone_number in self.clients:
            del self.clients[phone_number]

    def get_connected_user(self, phone_number):
        return self.connected_users.get(phone_number)