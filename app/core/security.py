from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from zxcvbn import zxcvbn
password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return password_hasher.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
    except InvalidHashError:
        return False


def validate_password_strength(password: str) -> str:
    if len(password) < 14:
        raise ValueError("La contraseña debe tener al menos 14 caracteres")
    result = zxcvbn(password)
    if result["score"] < 2:
        raise ValueError("La contraseña no es lo suficientemente segura")
    return password





 
  

