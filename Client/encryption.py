import logging
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import padding as sym_padding
from Client.config import SERVER_PUBLIC_KEY


def generate_or_load_ec_keypair(private_key_file, public_key_file):
    """Generate or load an ECDH key pair from files."""
    if os.path.exists(private_key_file) and os.path.exists(public_key_file):
        # Load the private key
        with open(private_key_file, 'rb') as private_file:
            private_key = serialization.load_pem_private_key(
                private_file.read(),
                password=None
            )

        # Load the public key
        with open(public_key_file, 'rb') as public_file:
            public_key = serialization.load_pem_public_key(
                public_file.read()
            )
    else:
        # Generate a new key pair
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()

        # Ensure the directory exists if a directory is specified
        private_key_dir = os.path.dirname(private_key_file)
        if private_key_dir and not os.path.exists(private_key_dir):
            os.makedirs(private_key_dir, exist_ok=True)

        # Serialize and save the private key
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(private_key_file, 'wb') as private_file:
            private_file.write(private_key_bytes)

        # Serialize and save the public key
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(public_key_file, 'wb') as public_file:
            public_file.write(public_key_bytes)

    return private_key, public_key


def serialize_public_key(public_key):
    """Serialize a public key for transmission."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def load_server_public_key(path=SERVER_PUBLIC_KEY):
    """Load the server's RSA public key from a PEM file."""
    try:
        with open(path, 'rb') as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(), backend=default_backend()
            )
        if not isinstance(public_key, RSAPublicKey):
            raise ValueError("Loaded key is not an RSA public key.")
        return public_key
    except Exception as e:
        logging.error(f"Failed to load server public key: {e}")
        raise

def load_public_key(public_key_bytes):
    """Load a public key from serialized bytes."""
    return serialization.load_pem_public_key(public_key_bytes, backend=default_backend())


def derive_symmetric_key(private_key, peer_public_key, salt=None):
    """Derive a symmetric key using ECDH shared secret and HKDF with a random salt."""
    if salt is None:
        salt = os.urandom(16)
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b'handshake data',
        backend=default_backend()
    )
    return hkdf.derive(shared_secret), salt


def encrypt_message(plaintext, symmetric_key):
    """Encrypt a message using AES-CBC."""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv, ciphertext

def decrypt_message(iv, ciphertext, symmetric_key):
    """Decrypt a message using AES-CBC."""
    try:
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
        return plaintext.decode()
    except ValueError as e:
        print(f"Decryption error: {e}")
        return None

def encrypt_data(data, public_key):
        return public_key.encrypt(
            data.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
