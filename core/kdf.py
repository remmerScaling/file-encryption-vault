from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

def derive_key(password: str, salt: bytes, iterations: int = 300_000) -> bytes:
    if not password:
        raise ValueError("Password cannot be empty")

    return PBKDF2(
        password.encode("utf-8"),
        salt,
        dkLen=32,             
        count=iterations,
        hmac_hash_module=SHA256
    )
