from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from core.kdf import derive_key

import json

BLOCK = 16


#delelig med 16 
def _pad(data:bytes) -> bytes:
    pad_len = BLOCK - (len(data) % BLOCK)
    return data + bytes([pad_len]) * pad_len

#fjern padding(dekryp)
def _unpad(data:bytes) -> bytes:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK:
        raise ValueError("invalid pad")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("invalid pad")
    return data[:-pad_len]


#krypteringen
def encrypt(input_file, output_file, password):
    #key = get_random_bytes(16)

    iv = get_random_bytes(16)
    salt = get_random_bytes(16)

    key = derive_key(password, salt)

    with open(input_file, 'rb') as f:
        plaintext = f.read()

    #pad_len = 16 - len(data) % 16
    #data += bytes([pad_len]) * pad_len

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = _pad(plaintext)
    ciphertext = cipher.encrypt(plaintext)

    with open(output_file, 'wb') as f:
        f.write(ciphertext)

    meta = {
        "salt": salt.hex(),
        "iv": iv.hex()
    }

    with open(output_file + ".meta", 'w') as f:
        json.dump(meta, f)

    print(f"Metadata : {output_file}.meta")
    print(f"Encryptet and saved as: {output_file}")




#dekrypteringen
def decrypt(input_file: str, output_file: str, password: str):


    with open(input_file + ".meta", "r") as f:
        meta = json.load(f)

    salt = bytes.fromhex(meta["salt"])
    iv = bytes.fromhex(meta["iv"])

    key = derive_key(password, salt)

    with open(input_file, "rb") as f:
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext)
    plaintext = _unpad(plaintext_padded)

    with open(output_file, "wb") as f:
        f.write(plaintext)

    print(f"Decrypted: {output_file}")