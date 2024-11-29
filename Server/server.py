import socket
import threading
from encryption import generate_rsa_keys, decrypt_message, encrypt_message
from config import BUFFER_SIZE
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

client_public_keys = {}  # Store public keys for connected clients

def handle_client(client_socket, client_address, server_private_key, server_public_key):
    try:
        print(f"New connection from {client_address}")

        # Receive client's public key
        client_public_key = client_socket.recv(BUFFER_SIZE)
        client_public_key = RSA.import_key(client_public_key)
        client_public_keys[client_address] = client_public_key

        # Send server's public key to the client
        client_socket.send(server_public_key)

        # Receive encrypted AES key
        encrypted_key = client_socket.recv(BUFFER_SIZE)
        cipher_rsa = PKCS1_OAEP.new(server_private_key)
        aes_key = cipher_rsa.decrypt(encrypted_key)

        # Communication loop
        while True:
            encrypted_data = client_socket.recv(BUFFER_SIZE)
            if not encrypted_data:
                break

            iv, ciphertext = encrypted_data[:16], encrypted_data[16:]
            message = decrypt_message(aes_key, iv, ciphertext)
            print(f"Received from {client_address}: {message}")

            # Respond to the client
            response = f"Server received: {message}"
            iv, encrypted_response = encrypt_message(aes_key, response)
            client_socket.send(iv + encrypted_response)

    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection closed with {client_address}")

def start_server(host, port):
    # Generate server keys
    server_private_key, server_public_key = generate_rsa_keys()
    print("Server keys generated.")

    # Start the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address, server_private_key, server_public_key)
        )
        thread.start()
