"""End to end encryption of files."""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher,modes
from cryptography.hazmat.primitives.ciphers.algorithms import AES256
from cryptography.hazmat.primitives.asymmetric import ec

nonce_ctr = 2**28

def encryption(plaintext: bytes, key_file_name: str) -> bytes:
    global nonce_ctr

    file = open(key_file_name, "r")
    key = file.read()

    key = key.encode('utf-8')
    cipher = AESGCM(key)

    header = nonce_ctr    
    ct = cipher.encrypt(nonce=bytes(str(nonce_ctr), 'ascii'),data=plaintext, associated_data=None)
    nonce_ctr += 1
    return header, ct

def keygen(fileName: str) -> bytes:
   file = open(fileName, "w")
   file.write(AESGCM.generate_key(128).hex())
   file.close()


def decryption(ciphertext: bytes, key_file_name: bytes) -> bytes:
    #maybe change keyfile type from bytes to str
    global nonce_ctr
    file = open(key_file_name, "r")
    key = file.read()
    key = key.encode('utf-8')

    cipher = AESGCM(key)
    pt = cipher.decrypt(data=ciphertext[1], nonce=ciphertext[0], associated_data=None)
    return pt 

##### not ready
def pad_file_name(file: str) -> str:
    padding_length = 2**16 - len(file)
    padding = bytes([padding_length]) * padding_length
    return file + padding