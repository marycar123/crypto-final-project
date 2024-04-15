
from etoe import decryption, encryption, keygen, enc_name, dec_name


def run(myFileName: str, keyFileName: str, nameKeyFileName: str) -> bool:

    #encrypts everything
    ct, my_file, encrypted_file_name = enc_and_upload(myFileName, keyFileName, nameKeyFileName)
    

    #decrypting        

    result = decryption(ciphertext = ct, keyFileName = keyFileName)

    #checking name decryption

    name_decrypt = dec_name(encrypted_file_name, nameKeyFileName)
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
    
def download_and_decrypt(downloadName, keyFileName, nameKeyFileName):

    #downloads the file from google drive
    file_download(downloadName)

    #breaks the given file name down to IV and encrypted
    encrypted_bytes_1 = bytes.fromhex(downloadName[:32])
    encrypted_bytes_2 = bytes.fromhex(downloadName[32:64])
    name_tuple = (encrypted_bytes_1, encrypted_bytes_2)

    #decypt and prase the name to get the origional file name
    name_decrypt = dec_name(name_tuple, nameKeyFileName)
    name_decrypt = name_decrypt.decode('utf-8')
    name_decrypt = name_decrypt[:(len(myFileName))]

    #download encrypted contents
    file = open(downloadName, "rb")
    ct = file.read()

    #parse the contents for nonce and encryption key for the file
    header = (ct[:9],ct[9:25])
    reconstructedCt =(header, ct[25:])   
    
    #decrypt the file contents
    result = decryption(ciphertext = reconstructedCt, keyFileName = keyFileName)

    #create a new file under the decrypted name and write the decypted contents to it
    decrypted_file = open(name_decrypt, "w")
    decrypted_file.write(result.decode('utf-8'))
    decrypted_file.close()
    os.remove(downloadName)

    return None



if __name__ == '__main__':
    # myFileName = input("Enter a file Name: ")
    # keyFileName = input("Where do you want to store your key? ")
    # nameKeyFileName = input("Where do you want the name key to be stored? ")

    myFileName = "thisFile.txt"
    keyFileName="key_thisFile.txt"
    nameKeyFileName = "nameKey_thisFile.txt"

    print(run(myFileName=myFileName, keyFileName=keyFileName, nameKeyFileName=nameKeyFileName))

