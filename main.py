
from etoe import decryption, encryption, keygen, enc_name, dec_name


def run(file_name: str, key_file_name: str, namekey_file_name: str) -> bool:

    #encrypts everything
    ct, my_file, iv, encrypted_file_name = enc_and_upload(file_name, key_file_name, namekey_file_name)
    

    #decrypting        

    result = decryption(ciphertext = ct, key_file_name = key_file_name, enc_title=encrypted_file_name)

    #checking name decryption

    name_decrypt = dec_name((iv,encrypted_file_name), namekey_file_name)
    name_decrypt = name_decrypt.decode('utf-8')
    name_decrypt = name_decrypt[:(len(file_name))]

    return result == my_file and name_decrypt == file_name


def enc_and_upload(file_name: str, key_file_name: str, namekey_file_name: str):
    file = open(file_name, "r")
    myFile = file.read()
    myFile = myFile.encode('utf-8')

    #Key for encrypting the file name
    keygen(namekey_file_name)
    file_name = file_name.encode('utf-8')
    #Encrypting the file name
    iv, encrypted_name = enc_name(file_name, namekey_file_name)

    #Key generation, will store key at this file 
    keygen(key_file_name)
    #encrypting file and giving the key store in that file's keyFile
    ct=encryption(myFile, key_file_name, encrypted_name)    
    



    encryptedFile = open(iv.hex()+encrypted_name.hex() + ".txt", "wb")

    encryptedFile.write(str(ct[0][0]).encode('utf-8'))
    encryptedFile.write(str(ct[0][1]).encode('utf-8'))
    encryptedFile.write(ct[1])
    encryptedFile.close()

    return ct, myFile, iv, encrypted_name
    


if __name__ == '__main__':
    # file_name = input("Enter a file Name: ")
    # key_file_name = input("Where do you want to store your key? ")
    # namekey_file_name = input("Where do you want the name key to be stored? ")

    file_name = "thisFile.txt"
    key_file_name="key_thisFile.txt"
    namekey_file_name = "nameKey_thisFile.txt"

    print(run(file_name=file_name, key_file_name=key_file_name, namekey_file_name=namekey_file_name))

