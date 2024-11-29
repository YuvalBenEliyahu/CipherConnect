from server import start_server
from config import HOST, PORT

if __name__ == "__main__":
    print("Initializing the server...")
    start_server(HOST, PORT)
