from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import json


#krypteringen
def encrypt(input_file, output_file, keyfile):
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    with open(input_file, 'rb') as f:
        data = f.read()

    pad_len = 16 - len(data) % 16
    data += bytes([pad_len]) * pad_len

    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(iv + encrypted)

    with open(keyfile, 'w') as f:
        json.dump({
            'key': key.hex(),
            'iv': iv.hex()
        }, f)

    print(f'Encryptet and saved as: {output_file}')
    print(f'Key and IV stored as: {keyfile}')




#dekrypteringen
def decrypt(input_file, output_file, keyfile):
    with open(keyfile, 'r') as f:
        keydata = json.load(f)

    key = bytes.fromhex(keydata['key'])
    iv = bytes.fromhex(keydata['iv'])

    with open(input_file, 'rb') as f:
        file_iv = f.read(16)
        encrypted = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)

    pad_len = decrypted[-1]
    decrypted = decrypted[:-pad_len]

    with open(output_file, 'wb') as f:
        f.write(decrypted)

    print(f'decrypted and stored as: {output_file}')

