import argparse
from Client.client import start_client
from config import HOST, PORT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Python client with CLI options.")
    parser.add_argument('--host', default=HOST, help=f"Server host to connect to. Default is {HOST}.")
    parser.add_argument('--port', type=int, default=PORT, help=f"Server port to connect to. Default is {PORT}.")
    args = parser.parse_args()

    start_client(host=args.host, port=args.port)
