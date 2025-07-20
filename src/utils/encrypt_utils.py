import os

from dotenv import load_dotenv
from cryptography.fernet import Fernet


"""Generate a new key """

# Load the key once at module load to avoid repeated load_dotenv calls
load_dotenv()

def get_fernet():
    key = os.getenv("FERNET_KEY")

    if not key:
        raise ValueError("Missing FERNET_KEY. Please set it in your .env file.")

    return Fernet(key.encode())


def encrypt_password(data: str) -> str:
    return get_fernet().encrypt(data.encode()).decode()

def decrypt_password(encrypted_data: str) -> str:
    return get_fernet().decrypt(encrypted_data.encode()).decode()