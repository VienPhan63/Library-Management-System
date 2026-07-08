import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, stored_password: str) -> bool:
    if not stored_password:
        return False

    if stored_password.startswith("$2"):
        return bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8"))

    return password == stored_password
