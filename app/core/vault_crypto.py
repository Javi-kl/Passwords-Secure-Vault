from argon2.low_level import hash_secret_raw, Type
from cryptography.fernet import Fernet
import os
import base64

VAULT_KEY_SIZE = 32  # 256 bits

def derive_vault_key(master_password: str, vault_salt: bytes) -> bytes:
    raw = hash_secret_raw(
        secret=master_password.encode(),
        salt=vault_salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=VAULT_KEY_SIZE,
        type=Type.ID,
    )
    return base64.urlsafe_b64encode(raw)

def generate_vault_salt()->bytes:
    return os.urandom(16)

def create_fernet(master_password:str,vault_salt:bytes) ->Fernet:
    key=derive_vault_key(master_password,vault_salt)
    return Fernet(key)

def encrypt_entry(fernet:Fernet, plaintext:str)->str:
    return fernet.encrypt(plaintext.encode()).decode()

def decrypt_entry(fernet:Fernet, ciphertext:str)->str:
    return fernet.decrypt(ciphertext.encode()).decode()