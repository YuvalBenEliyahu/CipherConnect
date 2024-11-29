import argparse
from Client.client import start_client
from config import HOST, PORT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Python client with CLI options.")
    parser.add_argument('--host', default=HOST, help="Server host to connect to. Default is 127.0.0.1.")
    parser.add_argument('--port', type=int, default=PORT, help="Server port to connect to. Default is 8080.")
    args = parser.parse_args()

    start_client(host=args.host1, port=args.port)