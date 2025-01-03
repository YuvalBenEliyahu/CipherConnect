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
        private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
        print(f"Loaded server private key: {private_key.private_numbers().d}")
        return private_key

def validate_public_key(pub_key):
    try:
        serialization.load_pem_public_key(pub_key.encode(), backend=default_backend())
        return True
    except (ValueError, InvalidKey):
        return False


def derive_key(password, salt=None, iterations=100000):
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    print(f"Derived key: {key.hex()}", f"Salt: {salt.hex()}")
    return key, salt


def decrypt_data(encrypted_data, private_key):
    """Decrypt data using the server's private key."""
    try:
        if isinstance(encrypted_data, str):
            encrypted_data = bytes.fromhex(encrypted_data)
        decrypted_key = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode('utf-8')
        print(f"Decrypted data: {decrypted_key}")
        return decrypted_key
    except (ValueError, TypeError, InvalidKey, InvalidSignature) as e:
        logging.error(f"Decryption failed: {e}")
        raise

def sign_data(data, private_key):
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

