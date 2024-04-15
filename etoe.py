"""End to end encryption of files."""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher,modes
from cryptography.hazmat.primitives.ciphers.algorithms import AES256
from cryptography.hazmat.primitives.asymmetric import ec

nonce_ctr = 2**28

def encryption(plaintext: bytes, keyFileName: str) -> bytes:
    #global nonce_ctr
    nonce_ctr = 2**28
    file = open(keyFileName, "r")
    key = file.read()

    key = key.encode('utf-8')
    cipher = AESGCM(key)

    #do we need a nonce???? associated data????
    header = (nonce_ctr, keyFileName)
    ct = cipher.encrypt(nonce=bytes(str(nonce_ctr), 'ascii'),data=plaintext, associated_data=keyFileName.encode('utf-8'))
    #nonce_ctr += 1
    return header, ct

def keygen(fileName: str) -> bytes:
   file = open(fileName, "w")
   file.write(AESGCM.generate_key(128).hex())
   file.close()


def decryption(ciphertext: bytes, keyFileName: bytes) -> bytes:
    global nonce_ctr
    file = open(keyFileName, "r")
    key = file.read()
    key = key.encode('utf-8')

    cipher = AESGCM(key)
    pt = cipher.decrypt(data=ciphertext[1], associated_data=ciphertext[0][1], nonce=ciphertext[0][0])
    return pt 


def enc_name(pt: bytes, keyFileName: str) -> bytes:
    file = open(keyFileName, "r")
    key = file.read()
    key = key.encode('utf-8')

    iv = os.urandom(16)

    cipher = Cipher(AES256(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    pt = pad_file_name(pt)
    ct = encryptor.update(pt) + encryptor.finalize()
    return (iv, ct)

def dec_name(ct: bytes, keyFileName: str) -> bytes: 
    file = open(keyFileName, "r")
    key = file.read()
    key = key.encode('utf-8')
    file.close()

    iv: bytes = b'0'
    cyt: bytes = b'0'

    iv, cyt = ct

    #check to see if this parses for the IV right
    cipher = Cipher(AES256(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    pt = decryptor.update(cyt) + decryptor.finalize()
    return pt

def pad_file_name(name: str) -> str:
    padding_length = 16 - (len(name) % 16)
    padding = bytes([padding_length]) * padding_length
    return name + padding