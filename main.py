
from etoe import decryption, encryption, keygen, enc_name, dec_name


def run(myFileName: str, keyFileName: str, nameKeyFileName: str) -> bool:

    #encrypts everything
    ct, my_file, encrypted_file = enc_and_upload(myFileName, keyFileName, nameKeyFileName)
    

    #decrypting        

    result = decryption(ciphertext = ct, keyFileName = keyFileName)

    #checking name decryption

    name_decrypt = dec_name(encrypted_file, nameKeyFileName)
    name_decrypt = name_decrypt.decode('utf-8')
    name_decrypt = name_decrypt[:(len(myFileName))]


    return result == my_file and name_decrypt == myFileName


def enc_and_upload(myFileName: str, keyFileName: str, nameKeyFileName: str):
    file = open(myFileName, "r")
    myFile = file.read()
    myFile = myFile.encode('utf-8')

    #Key generation, will store key at this file 
    keygen(keyFileName)
    #encrypting file and giving the key store in that file's keyFile
    ct=encryption(myFile, keyFileName)    
    

    keygen(nameKeyFileName)
    myFileName = myFileName.encode('utf-8')
    encrypted_name = enc_name(myFileName, nameKeyFileName)

    encryptedFile = open(encrypted_name[0].hex()+encrypted_name[1].hex() + ".txt", "wb")

    encryptedFile.write(str(ct[0][0]).encode('utf-8'))
    encryptedFile.write(str(ct[0][1]).encode('utf-8'))
    encryptedFile.write(ct[1])
    encryptedFile.close()

    return ct, myFile, encrypted_name
    


if __name__ == '__main__':
    # myFileName = input("Enter a file Name: ")
    # keyFileName = input("Where do you want to store your key? ")
    # nameKeyFileName = input("Where do you want the name key to be stored? ")

    myFileName = "thisFile.txt"
    keyFileName="key_thisFile.txt"
    nameKeyFileName = "nameKey_thisFile.txt"

    print(run(myFileName=myFileName, keyFileName=keyFileName, nameKeyFileName=nameKeyFileName))

