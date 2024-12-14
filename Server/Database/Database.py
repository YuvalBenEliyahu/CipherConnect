import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_filename="users.db"):
        self.db_filename = db_filename
        self.conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Create users table with an additional column for salt
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                phone_number TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                password TEXT NOT NULL,
                public_key TEXT,
                salt BLOB NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
               CREATE TABLE IF NOT EXISTS offline_messages (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   sender_phone_number TEXT NOT NULL,
                   receiver_phone_number TEXT NOT NULL,
                   message TEXT NOT NULL,
                   timestamp TEXT NOT NULL,
                   FOREIGN KEY (receiver_phone_number) REFERENCES users(phone_number)
               )
           ''')
        self.conn.commit()

    def close_connection(self):
        """Close the database connection explicitly."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def add_user(self, name, last_name, phone_number, password, public_key, salt):
        # Check if the phone number already exists
        if self.get_user_by_phone_number(phone_number):
            error_message = "Error: Phone number already exists."
            print(error_message)
            return error_message

        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            self.cursor.execute('''
                INSERT INTO users (phone_number, name, last_name, password, public_key, salt, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (phone_number, name, last_name, password, public_key, salt, created_at))
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
            SELECT name, last_name, phone_number, password, public_key, salt, created_at
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
                "salt": result[5],
                "created_at": result[6]
            }
        return None

    def add_offline_message(self, sender_phone_number, receiver_phone_number, message, timestamp):
        self.cursor.execute('''
            INSERT INTO offline_messages (sender_phone_number, receiver_phone_number, message, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (sender_phone_number, receiver_phone_number, message, timestamp))
        self.conn.commit()

    def get_offline_messages(self, receiver_phone_number):
        self.cursor.execute('''
            SELECT sender_phone_number, message, timestamp
            FROM offline_messages
            WHERE receiver_phone_number = ?
        ''', (receiver_phone_number,))
        messages = self.cursor.fetchall()
        self.cursor.execute('''
            DELETE FROM offline_messages
            WHERE receiver_phone_number = ?
        ''', (receiver_phone_number,))
        self.conn.commit()
        return messages

    def delete_offline_messages(self, receiver_phone_number):
        """Delete offline messages for a specific receiver."""
        self.cursor.execute('''
            DELETE FROM offline_messages
            WHERE receiver_phone_number = ?
        ''', (receiver_phone_number,))
        self.conn.commit()