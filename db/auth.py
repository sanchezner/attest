import hashlib


def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()