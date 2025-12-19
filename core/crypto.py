from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from core.kdf import derive_key

import os
import json


#krypteringen
def encrypt(input_file, output_file, password):
    #key = get_random_bytes(16)
    iv = get_random_bytes(16)
    salt = get_random_bytes(16)
    key = derive_key(password, salt)


    with open(input_file, 'rb') as f:
        data = f.read()

    pad_len = 16 - len(data) % 16
    data += bytes([pad_len]) * pad_len

    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)

    with open(output_file + ".meta", 'w') as f:
        json.dump({
            'salt': salt.hex(),
            'iv': iv.hex()
        }, f)

    print(f'Encryptet and saved as: {output_file}')




#dekrypteringen
def decrypt(input_file, output_file, password):
    with open(input_file, 'r') as f:
        keydata = json.load(f)

    #key = bytes.fromhex(keydata['key'])
    salt = bytes.fromhex(keydata['salt'])
    key = derive_key(password, salt)
    iv = bytes.fromhex(keydata['iv'])

    with open(input_file, 'rb') as f:
        #file_iv = f.read(16)
        encrypted = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)

    pad_len = decrypted[-1]
    decrypted = decrypted[:-pad_len]

    with open(output_file, 'wb') as f:
        f.write(decrypted)

    print(f'decrypted and stored as: {output_file}')

