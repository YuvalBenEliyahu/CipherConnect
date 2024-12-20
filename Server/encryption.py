import logging
import os

from cryptography.exceptions import InvalidKey, InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from Server.config import SERVER_PRIVATE_KEY_PATH


def load_server_private_key(path=SERVER_PRIVATE_KEY_PATH):
    with open(path, 'rb') as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

def validate_public_key(pub_key):
    try:
        # Attempt to load the public key
        serialization.load_pem_public_key(pub_key.encode(), backend=default_backend())
        return True
    except (ValueError, InvalidKey):
        return False


def derive_key(password, salt=None, iterations=100000):
    if salt is None:
        salt = os.urandom(16)  # Generate a new salt if not provided
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key, salt


def decrypt_data(encrypted_data, private_key):
    """Decrypt data using the server's private key."""
    try:
        if isinstance(encrypted_data, str):
            encrypted_data = bytes.fromhex(encrypted_data)
        return private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode('utf-8')
    except (ValueError, TypeError, InvalidKey, InvalidSignature) as e:
        logging.error(f"Decryption failed: {e}")
        raise