class RegistrationHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def handle_registration(self, payload):
        # Parse registration data
        parts = payload.split(",")
        if len(parts) < 4 or len(parts) > 5:
            return "ERROR: Invalid registration data format."

        name, last_name, phone_number, password = parts[:4]
        public_key = parts[4] if len(parts) == 5 else None

        # Add user to the database
        if self.db_manager.add_user(name, last_name, phone_number, password, public_key):
            return f"SUCCESS: User {name} {last_name} registered."
        else:
            return "ERROR: Phone number already exists."
