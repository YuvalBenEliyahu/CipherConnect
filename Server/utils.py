import re
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey


def pad(data, block_size):
    padding_length = block_size - len(data) % block_size
    return data + bytes([padding_length] * padding_length)


def unpad(data, block_size):
    padding_length = data[-1]
    if padding_length > block_size:
        raise ValueError("Invalid padding")
    return data[:-padding_length]


def password_check(passwd):
    # Check if password length is between 6 and 20 characters
    if (6 <= len(passwd) <= 20 and
            # Check if password contains at least one digit
            re.search(r'\d', passwd) and
            # Check if password contains at least one uppercase letter
            re.search(r'[A-Z]', passwd) and
            # Check if password contains at least one lowercase letter
            re.search(r'[a-z]', passwd) and
            # Check if password contains at least one special symbol
            re.search(r'[$@#%!&*^?:;,./<>|~`+\-=_{}[\]()]', passwd)):
        return True
    return False


def validate_public_key(pub_key):
    try:
        # Attempt to load the public key
        serialization.load_pem_public_key(pub_key.encode(), backend=default_backend())
        return True
    except (ValueError, InvalidKey):
        return False
