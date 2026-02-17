import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: bytes) -> bool:
    """Verify a password against a hashed password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
