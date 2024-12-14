import argparse

from Client.client import start_client
from Client.Database.Database import ClientDatabaseManager
from config import HOST, PORT, CLIENT_CHAT_TABLE

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Python client with CLI options.")
    parser.add_argument('--host', default=HOST, help=f"Server host to connect to. Default is {HOST}.")
    parser.add_argument('--port', type=int, default=PORT, help=f"Server port to connect to. Default is {PORT}.")
    parser.add_argument('--db_filename', default=CLIENT_CHAT_TABLE,
                        help=f"Database filename to use. Default is {CLIENT_CHAT_TABLE}.")
    args = parser.parse_args()

    client_db = ClientDatabaseManager(db_filename=args.db_filename)
    start_client(host=args.host, port=args.port, db_manager=client_db)
