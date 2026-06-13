import hashlib
import os


def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"$sha256${salt}${digest}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password.startswith("$sha256$"):
        return False

    parts = hashed_password.split("$")
    if len(parts) != 4:
        return False

    salt = parts[2]
    digest = parts[3]
    expected = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
    return digest == expected
