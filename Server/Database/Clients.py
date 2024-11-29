class Clients:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.clients = {}  # In-memory cache for clients

    def add_client(self, name, last_name, phone_number, password):
        if self.db_manager.add_user(name, last_name, phone_number, password):
            self.clients[phone_number] = {
                "name": name,
                "last_name": last_name,
                "phone_number": phone_number
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
