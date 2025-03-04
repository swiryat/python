# Import necessary modules
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Generate a random key for TripleDES
key = os.urandom(16)  # Use 16 bytes for TripleDES

# Initialize the TripleDES cipher
cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())

# Create a cipher object
encryptor = cipher.encryptor()

# Encrypt the message
message = b"Secret message"
padder = padding.PKCS7(64).padder()
padded_data = padder.update(message) + padder.finalize()
ciphertext = encryptor.update(padded_data) + encryptor.finalize()

print("Зашифрованное сообщение:", ciphertext)  # Print the encrypted message

