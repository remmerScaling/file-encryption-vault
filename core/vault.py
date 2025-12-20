import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from core.crypto import _pad, _unpad, BLOCK
from core.kdf import derive_key

VAULT_VERSION = 1

def vault_create(vault_path: str, password: str) -> dict:

    salt = get_random_bytes(16)
    iv = get_random_bytes(16)
    key = derive_key(password, salt)

    vault_data = {
        "version": VAULT_VERSION,
        "files": [],
        "notes": []
    }

    plaintext = json.dumps(vault_data).encode("utf-8")
    plaintext = _pad(plaintext)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext)

    vault_file = {
        "version": VAULT_VERSION,
        "salt": salt.hex(),
        "iv": iv.hex(),
        "ciphertext": ciphertext.hex()
    }

    with open(vault_path, "w") as f:
        json.dump(vault_file, f)

    return vault_data


def vault_open(vault_path: str, password: str) -> dict:

    with open(vault_path, "r") as f:
        vault_file = json.load(f)

    salt = bytes.fromhex(vault_file["salt"])
    iv = bytes.fromhex(vault_file["iv"])
    ciphertext = bytes.fromhex(vault_file["ciphertext"])

    key = derive_key(password, salt)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext)
    plaintext = _unpad(plaintext_padded)

    vault_data = json.loads(plaintext.decode("utf-8"))
    return vault_data


def vault_save(vault_path: str, password: str, vault_data: dict):

    with open(vault_path, "r") as f:
        vault_file = json.load(f)

    salt = bytes.fromhex(vault_file["salt"])
    iv = get_random_bytes(16) 
    key = derive_key(password, salt)

    plaintext = json.dumps(vault_data).encode("utf-8")
    plaintext = _pad(plaintext)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext)

    vault_file["iv"] = iv.hex()
    vault_file["ciphertext"] = ciphertext.hex()

    with open(vault_path, "w") as f:
        json.dump(vault_file, f)



