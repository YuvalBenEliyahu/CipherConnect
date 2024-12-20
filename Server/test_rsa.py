from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization


def test_rsa_keypair(private_key, public_key):
    """
    Test the RSA key pair for encryption and decryption.

    Args:
        private_key: The RSA private key.
        public_key: The RSA public key.
    """
    try:
        # Sample message
        message = "Test message for RSA encryption"

        # Encrypt with public key
        encrypted = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Encryption successful!")

        # Decrypt with private key
        decrypted = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Decryption successful!")
        print(f"Decrypted message: {decrypted.decode()}")
    except Exception as e:
        print(f"Key pair test failed: {e}")

def load_private_key(private_key_path):
    """Load an RSA private key from a PEM file."""
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def load_public_key(public_key_path):
    """Load an RSA public key from a PEM file."""
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

# Test the generated key pair
test_rsa_keypair(load_private_key("server_private_key.pem"), load_public_key("../Client/server_public_key.pem"))
