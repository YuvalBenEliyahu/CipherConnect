import sqlite3
from Client.config import CLIENT_CHAT_TABLE


class ClientDatabaseManager:
    def __init__(self, db_filename=CLIENT_CHAT_TABLE):
        self.db_filename = db_filename
        self.conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_chats_table()

    def create_chats_table(self):
        """Create the chats table if it does not exist."""
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {CLIENT_CHAT_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_chat_message(self, phone_number, message, timestamp):
        """Add a chat message to the database."""
        self.cursor.execute(f'''
            INSERT INTO {CLIENT_CHAT_TABLE} (phone_number, message, timestamp)
            VALUES (?, ?, ?)
        ''', (phone_number, message, timestamp))
        self.conn.commit()

    def get_chat_messages(self, phone_number):
        """Retrieve chat messages for a specific phone number."""
        self.cursor.execute(f'''
            SELECT message, timestamp
            FROM {CLIENT_CHAT_TABLE}
            WHERE phone_number = ?
            ORDER BY timestamp
        ''', (phone_number,))
        return self.cursor.fetchall()

    def delete_chat(self, phone_number):
        """Delete chat messages for a specific phone number."""
        self.cursor.execute(f'''
            DELETE FROM {CLIENT_CHAT_TABLE}
            WHERE phone_number = ?
        ''', (phone_number,))
        self.conn.commit()

    def delete_all_chats(self):
        """Delete all chat messages."""
        self.cursor.execute(f'DELETE FROM {CLIENT_CHAT_TABLE}')
        self.conn.commit()

    def get_all_phone_numbers_with_chats(self):
        """Retrieve all phone numbers with chat messages."""
        self.cursor.execute(f'''
            SELECT DISTINCT phone_number
            FROM {CLIENT_CHAT_TABLE}
        ''')
        return [row[0] for row in self.cursor.fetchall()]
