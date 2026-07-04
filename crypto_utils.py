"""
main functions of encrypting and decrypting of passwords
"""
import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_password(plain_text : str, master_password: str) -> str:
    "encrypt a text with AES-GCM"
    key = master_password.encode().ljust(32, b'\0')[:32]

    cipher = AES.new(key, AES.MODE_GCM)

    ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode())

    combined = cipher.nonce + tag + ciphertext
    return base64.b64encode(combined).decode()

def decrypt_password(encrtypted_b64: str, master_password: str)-> str:
    "decrypt a text with AES-GCM"

    key = master_password.encode().ljust(32, b'\0')[:32]

    combined = base64.b64decode(encrtypted_b64)

    nonce = combined[:16]
    tag = combined[16:32]
    ciphertext = combined[32:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode()