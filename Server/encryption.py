from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import hashlib
from utils import pad, unpad

KEY_SIZE = 32
SALT_SIZE = 16
ITERATIONS = 100000

def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return RSA.import_key(private_key), public_key

def encrypt_message(key, plaintext):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return iv, ciphertext

def decrypt_message(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

def generate_aes_key(password):
    salt = get_random_bytes(SALT_SIZE)
    return PBKDF2(password, salt, dkLen=KEY_SIZE, count=ITERATIONS, hmac_hash_module=hashlib.sha256), salt
