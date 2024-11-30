import json
import re
import logging

class LoginHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def handle_login(self, payload, client_address):
        logging.debug("Handling login with payload: %s from %s", payload, client_address)
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            logging.error("Invalid JSON format from %s", client_address)
            return "ERROR: Invalid JSON format."

        phone_number = data.get("phone_number")
        password = data.get("password")

        if not phone_number or not password:
            logging.error("Missing login data from %s", client_address)
            return "ERROR: Missing login data."

        # Retrieve user from the database
        user = self.db_manager.get_user_by_phone_number(phone_number)
        if not user:
            logging.error("User not found from %s", client_address)
            return "ERROR: User not found."

        # Check if the password matches
        if user["password"] != password:
            logging.error("Incorrect password from %s", client_address)
            return "ERROR: Incorrect password."

        logging.info("User %s %s logged in successfully from %s", user['name'], user['last_name'], client_address)
        return f"SUCCESS: User {user['name']} {user['last_name']} logged in."