
from etoe import decryption, encryption, keygen, enc_name, dec_name
from upload_download import file_upload, file_download
import os


def run(myFileName: str, keyFileName: str, nameKeyFileName: str) -> bytes:

    #encrypts everything
    ct, my_file, encrypted_file_name = enc_and_upload(myFileName, keyFileName, nameKeyFileName)
    

    #decrypting        

    # result = decryption(ciphertext = ct, keyFileName = keyFileName)

    # #checking name decryption

    # name_decrypt = dec_name(encrypted_file_name, nameKeyFileName)
    # name_decrypt = name_decrypt.decode('utf-8')
    # name_decrypt = name_decrypt[:(len(myFileName))]

    # return result == my_file and name_decrypt == myFileName
    return encrypted_file_name


def enc_and_upload(myFileName: str, keyFileName: str, nameKeyFileName: str):
    file = open(myFileName, "r")
    myFile = file.read()
    myFile = myFile.encode('utf-8')

    keygen(nameKeyFileName)
    myFileName = myFileName.encode('utf-8')
    encrypted_name = enc_name(myFileName, nameKeyFileName)

    #Key generation, will store key at this file 
    keygen(keyFileName)
    #encrypting file and giving the key store in that file's keyFile
    ct=encryption(myFile, keyFileName,encrypted_name[1])    
    



    combinedName = encrypted_name[0].hex()+encrypted_name[1].hex() + ".txt"
    encryptedFile = open(combinedName, "wb")

    encryptedFile.write(str(ct[0][0]).encode('utf-8'))
    #encryptedFile.write(str(ct[0][1]).encode('utf-8'))
    encryptedFile.write(ct[1])
    encryptedFile.close()
    print("testing****************************")
    print(f"Name: {encrypted_name[1]}")
    print(f"Nonce: {ct[0][0]}")
    print(f"KeyFile Name: {ct[0][1]}")
    print(f"CT: {ct[1]}")

    file_upload([combinedName])
    os.remove(combinedName)

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

    print(name_decrypt)

    #download encrypted contents
    file = open(downloadName, "rb")
    ct = file.read()

    #parse the contents for nonce and encryption key for the file
    #header = (ct[:9],ct[9:25])
    header = (ct[:9], encrypted_bytes_2)
    reconstructedCt =(header, ct[9:])
    print("testing****************************")
    print(f"Name: {encrypted_bytes_2}")
    print(f"Nonce: {reconstructedCt[0][0]}")
    print(f"KeyFile Name: {reconstructedCt[0][1]}")
    print(f"CT: {reconstructedCt[1]}")  

    
    #decrypt the file contents
    result = decryption(ciphertext = reconstructedCt, keyFileName = keyFileName)

    print(name_decrypt)
    #create a new file under the decrypted name and write the decypted contents to it
    decrypted_file = open(name_decrypt, "w")
    decrypted_file.write(result.decode('utf-8'))
    decrypted_file.close()
    #os.remove(decrypted_file)

    return None



if __name__ == '__main__':
    # myFileName = input("Enter a file Name: ")
    # keyFileName = input("Where do you want to store your key? ")
    # nameKeyFileName = input("Where do you want the name key to be stored? ")

    myFileName = "test_2.txt"
    keyFileName="test2_1_key.txt"
    nameKeyFileName = "testName2_1_key.txt"

    #print(run(myFileName=myFileName, keyFileName=keyFileName, nameKeyFileName=nameKeyFileName))
    download_and_decrypt("c22813fc62ea3cfe96c260c4cbdfdb62398a6d6dceac2bca4f3d35b7c030809b.txt",keyFileName,nameKeyFileName)

