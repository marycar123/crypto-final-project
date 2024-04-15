
from etoe import decryption, encryption, keygen, enc_name, dec_name
from upload_download import file_upload, file_download
import os

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
    
def download_and_decrypt(download_name: str, key_file_name: str, name_key_file_name: str):

    #downloads the file from google drive
    file_download(download_name)

    #breaks the given file name down to IV and encrypted
    encrypted_bytes_1 = bytes.fromhex(download_name[:32])
    encrypted_bytes_2 = bytes.fromhex(download_name[32:64])
    name_tuple = (encrypted_bytes_1, encrypted_bytes_2)

    #decypt and prase the name to get the origional file name
    name_decrypt = dec_name(name_tuple, name_key_file_name)
    name_decrypt = name_decrypt.decode('utf-8')
    name_decrypt = name_decrypt[:(len(name_key_file_name))]

    #download encrypted contents
    file = open(download_name, "rb")
    ct = file.read()

    #parse the contents for nonce and encryption key for the file
    header = (ct[:9],ct[9:25])
    reconstructedCt =(header, ct[25:])   
    
    #decrypt the file contents
    result = decryption(ciphertext = reconstructedCt, key_file_name=key_file_name,enc_title= encrypted_bytes_1)

    #create a new file under the decrypted name and write the decypted contents to it
    decrypted_file = open(name_decrypt, "w")
    decrypted_file.write(result.decode('utf-8'))
    decrypted_file.close()
    os.remove(download_name)

    return None



if __name__ == '__main__':
    # file_name = input("Enter a file Name: ")
    # key_file_name = input("Where do you want to store your key? ")
    # namekey_file_name = input("Where do you want the name key to be stored? ")

    file_name = "thisFile.txt"
    key_file_name="key_thisFile.txt"
    namekey_file_name = "nameKey_thisFile.txt"

    #print(run(myFileName=myFileName, keyFileName=keyFileName, nameKeyFileName=nameKeyFileName))
    download_and_decrypt("23f2673bc3f956ba88e673fb4c83dd067943500b429f0aae732d36315bedf13d.txt",key_file_name, namekey_file_name)

