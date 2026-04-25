import base64
import os

from argon2.low_level import Type, hash_secret_raw
from cryptography.fernet import Fernet

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


def generate_vault_salt() -> bytes:
    return os.urandom(16)


def create_fernet(master_password: str, vault_salt: bytes) -> Fernet:
    key = derive_vault_key(master_password, vault_salt)
    return Fernet(key)


def encrypt_entry(fernet: Fernet, plaintext: str) -> str:
    return fernet.encrypt(plaintext.encode()).decode()


def decrypt_entry(fernet: Fernet, ciphertext: str) -> str:
    return fernet.decrypt(ciphertext.encode()).decode()


def re_encrypt(ciphertext: str, old_fernet: Fernet, new_fernet: Fernet) -> str:
    """Descifrar con old_fernet y vuelve a cifrar con new_fernet"""
    plaintext = decrypt_entry(old_fernet, ciphertext)
    return encrypt_entry(new_fernet, plaintext)
