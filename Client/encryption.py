import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Define file paths in the Client folder
private_key_file = 'Client/Data/private_key.pem'
public_key_file = 'Client/Data/public_key.pem'

# Define a password for encryption
password = b"your-secure-password"

# Function to generate and save keys
def generate_and_save_keys():
    # Ensure the directory exists
    os.makedirs(os.path.dirname(private_key_file), exist_ok=True)

    # Generate an ECC private key
    private_key_fl = ec.generate_private_key(
        ec.SECP256R1()
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

    # Serialize and save the private key with encryption
    private_key_pem = private_key_fl.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(key)
    )

    # Generate the public key from the private key
    public_key = private_key_fl.public_key()

    # Serialize and save the public key
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Write the private key to a file
    with open(private_key_file, 'wb') as private_key_fl:
        private_key_fl.write(private_key_pem)

    # Write the public key to a file
    with open(public_key_file, 'wb') as public_key_fl:
        public_key_fl.write(public_key_pem)

    return private_key_pem, public_key_pem

# Check if the key files exist
if os.path.exists(private_key_file) and os.path.exists(public_key_file):
    # Load the private key from the file
    with open(private_key_file, 'rb') as private_file:
        private_key_pem = private_file.read()

    # Load the public key from the file
    with open(public_key_file, 'rb') as public_file:
        public_key_pem = public_file.read()
else:
    # Generate and save the keys
    private_key_pem, public_key_pem = generate_and_save_keys()