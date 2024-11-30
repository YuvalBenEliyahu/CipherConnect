import sqlite3
from datetime import datetime


class ClientDatabaseManager:
    def __init__(self, db_filename="client_chats.db"):
        self.db_filename = db_filename
        self.conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_chats_table()

    def create_chats_table(self):
        """Create the chats table if it does not exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                phone_number TEXT PRIMARY KEY,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_chat_message(self, phone_number, message, timestamp):
        """Add a chat message to the database."""
        self.cursor.execute('''
            INSERT INTO chats (phone_number, message, timestamp)
            VALUES (?, ?, ?)
            ON CONFLICT(phone_number) DO UPDATE SET
            message=excluded.message,
            timestamp=excluded.timestamp
        ''', (phone_number, message, timestamp))
        self.conn.commit()

    def get_chat_messages(self, phone_number):
        """Retrieve chat messages for a specific phone number."""
        self.cursor.execute('''
            SELECT message, timestamp
            FROM chats
            WHERE phone_number = ?
            ORDER BY timestamp
        ''', (phone_number,))
        return self.cursor.fetchall()

    def delete_chat(self, phone_number):
        """Delete chat messages for a specific phone number."""
        self.cursor.execute('''
            DELETE FROM chats
            WHERE phone_number = ?
        ''', (phone_number,))
        self.conn.commit()

    def delete_all_chats(self):
        """Delete all chat messages."""
        self.cursor.execute('DELETE FROM chats')
        self.conn.commit()

    def get_all_phone_numbers_with_chats(self):
        """Retrieve all phone numbers with chat messages."""
        self.cursor.execute('''
            SELECT DISTINCT phone_number
            FROM chats
        ''')
        return [row[0] for row in self.cursor.fetchall()]