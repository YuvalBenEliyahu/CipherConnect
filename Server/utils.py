import re
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

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