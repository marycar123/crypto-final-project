
from etoe import decryption, encryption, keygen


def run(myFileName: str, keyFileName: str) -> bool:

    file = open(myFileName, "r")
    myFile = file.read()
    myFile = myFile.encode('utf-8')
    

    #Key generation, will store key at this file 
    key=keygen(keyFileName)
    #encrypting file and giving the key store in that file's keyFile
    ct=encryption(myFile, keyFileName)     
    #decrypting        
    result = decryption(ciphertext = ct, keyFileName = keyFileName)

    return result == myFile



if __name__ == '__main__':
    myFileName = input("Enter a file Name: ")
    keyFileName = input("Where do you want to store your key? ")

    print(run(myFileName=myFileName, keyFileName=keyFileName))

