class RegistrationHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def handle_registration(self, payload):
        # Parse registration data
        parts = payload.split(",")
        if len(parts) != 5:
            return "ERROR: Invalid registration data format."

        name, last_name, phone_number, password, public_key = parts

        # Add user to the database
        result = self.db_manager.add_user(name, last_name, phone_number, password, public_key)
        if "Error" in result:
            return result
        else:
            return f"SUCCESS: User {name} {last_name} registered."
