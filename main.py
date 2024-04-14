
from etoe import decryption, encryption, keygen, enc_name, dec_name


def run(myFileName: str, keyFileName: str, nameKeyFileName: str) -> bool:

    file = open(myFileName, "r")
    myFile = file.read()
    myFile = myFile.encode('utf-8')

    #Key generation, will store key at this file 
    keygen(keyFileName)
    #encrypting file and giving the key store in that file's keyFile
    ct=encryption(myFile, keyFileName)     
    #TODO: encrypt file name 

    keygen(nameKeyFileName)
    myFileName = myFileName.encode('utf-8')
    encrypted_name = enc_name(myFileName, nameKeyFileName)



    encryptedFile = open(encrypted_name + ".txt", "w")
    encryptedFile.write(ct)
    encryptedFile.close()

    #decrypting        

    result = decryption(ciphertext = ct, keyFileName = keyFileName)

    return result == myFile



if __name__ == '__main__':
    # myFileName = input("Enter a file Name: ")
    # keyFileName = input("Where do you want to store your key? ")
    # nameKeyFileName = input("Where do you want the name key to be stored? ")

    myFileName = "thisFile.txt"
    keyFileName="key_thisFile.txt"
    nameKeyFileName = "nameKey_thisFile.txt"

    print(run(myFileName=myFileName, keyFileName=keyFileName, nameKeyFileName=nameKeyFileName))

