import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_filename="users.db"):
        self.db_filename = db_filename
        self.conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Create users table with an additional column for publicKey
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                phone_number TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                password TEXT NOT NULL,
                public_key TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def close_connection(self):
        """Close the database connection explicitly."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def add_user(self, name, last_name, phone_number, password, public_key):
        # Check if the phone number already exists
        if self.get_user_by_phone_number(phone_number):
            error_message = "Error: Phone number already exists."
            print(error_message)
            return error_message

        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            self.cursor.execute('''
                INSERT INTO users (phone_number, name, last_name, password, public_key, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (phone_number, name, last_name, password, public_key, created_at))
            self.conn.commit()
            success_message = f"User {name} {last_name} added successfully."
            print(success_message)
            return success_message
        except sqlite3.IntegrityError as e:
            error_message = f"Error: {str(e)}"
            print(error_message)
            return error_message

    def get_user_by_phone_number(self, phone_number):
        self.cursor.execute('''
            SELECT name, last_name, phone_number, password, public_key, created_at
            FROM users
            WHERE phone_number = ?
        ''', (phone_number,))
        result = self.cursor.fetchone()
        if result:
            return {
                "name": result[0],
                "last_name": result[1],
                "phone_number": result[2],
                "password": result[3],
                "public_key": result[4],
                "created_at": result[5]
            }
        return None
