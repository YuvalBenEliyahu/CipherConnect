import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Define a password for encryption
password = b"your-secure-password"


# Function to generate and save keys in RAM
def generate_keys():
    # Generate an RSA private key
    private_key_fl = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Generate a salt
    salt = os.urandom(16)

    # Derive a key from the password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)

    # Serialize the private key with encryption
    private_key_pem = private_key_fl.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(key)
    )

    # Generate the public key from the private key
    public_key = private_key_fl.public_key()

    # Serialize the public key
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_pem, public_key_pem

# Generate and store the keys in RAM
private_key_pem, public_key_pem = generate_keys()