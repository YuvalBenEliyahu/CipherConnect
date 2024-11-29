import argparse

from Client.client import start_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Python client with CLI options.")
    parser.add_argument('--host', default='127.0.0.1', help="Server host to connect to. Default is 127.0.0.1.")
    parser.add_argument('--port', type=int, default=65432, help="Server port to connect to. Default is 65432.")
    args = parser.parse_args()

    start_client(host=args.host, port=args.port)