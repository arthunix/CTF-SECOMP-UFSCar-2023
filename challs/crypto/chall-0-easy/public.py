#!/usr/bin/env python3

import time
from Crypto.Util.number import long_to_bytes
import hashlib
# from utils import listener

FLAG = b'SecomPWN23{?????????????????????????????}'


def generate_key():
    current_time = int(time.time())
    key = long_to_bytes(current_time)
    return hashlib.sha256(key).digest()


def encrypt(b):
    key = generate_key() + generate_key()[0:9]
    assert len(b) <= len(key), "Data package too large to encrypt"
    ciphertext = b''
    for i in range(len(b)):
        ciphertext += bytes([b[i] ^ key[i]])
    return ciphertext.hex()


def challenge(your_input):
    if not 'action' in your_input:
        return {"error": "You must send an action to this server"}

    elif your_input['action'] == 'get_flag':
        return {"encrypted_flag": encrypt(FLAG)}

    elif your_input['action'] == 'encrypt_data':
        your_input['data'] += '0' if len(your_input['data']) % 2 == 1 else ''
        input_data = bytes.fromhex(your_input['data'])
        return {"encrypted_data": encrypt(input_data)}

    else:
        return {"error": "Invalid option"}


"""
When you connect, the 'challenge' function will be called on your JSON
input.
"""
