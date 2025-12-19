from Crypto.Protocol.KDF import PBKDF2                  #password-based key derivation function 2
from Crypto.Hash import SHA256


def derive_key(password: str, salt: bytes, iterations: int = 300_000) -> bytes:
    pass
