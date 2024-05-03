
from etoe import decryption, encryption, keygen
import oram
from upload_download import file_upload, file_download
from drive_setup import drive_wipe, dummy_data_upload
import os

key_file: str = "key_thisFile.txt"

def setup_drive(dummy_num: int):
    global key_file
    drive_wipe()
    dummy_data_upload(dummy_num,key_file)



def enc_and_upload(my_file_name: str):
    global key_file
    file = open(my_file_name, "r")
    my_file = file.read()
    my_file = my_file.encode('utf-8')
    file.close()


    #Key generation, will store key at this file 
    #encrypting file and giving the key store in that file's keyFile
    nonce, ct=encryption(my_file, key_file)   

    #maybe delete everything in the file before
    encrypted_file = open(my_file_name, "wb")
    encrypted_file.write(str(nonce).encode('utf-8'))
    encrypted_file.write(ct)
    encrypted_file.close()

    file_upload([my_file_name])
    os.remove(my_file_name)

    return ct, my_file
    
def download_and_decrypt(download_names: list[str], file_names: list[str]):
    global key_file
    for i in range(len(download_names)):
        #downloads the file from google drive
        file_download(download_names[i])

        #download encrypted contents
        file = open(download_names[i], "rb")
        ct = file.read()

        #parse the contents for nonce and encryption key for the file
        header = (ct[0:9])
        reconstructed_ct =(header, ct[9:])  
        
        #decrypt the file contents
        result = decryption(reconstructed_ct, key_file)

        #create a new file under the decrypted name and write the decypted contents to it
        decrypted_file = open(file_names[i], "w")
        decrypted_file.write(result.decode('utf-8'))
        decrypted_file.close()
    #os.remove(decrypted_file)

    return None



if __name__ == '__main__':
    newUser: bool = False
    oram = oram.Oram(6, 2**16)

    start=input("Do you have a key file set up? Y/N \n")
    if start == "N":
        newUser = True
        keyFile = input("Where would you like to put the key? (file name) \n")
        keygen(keyFile)
        setup_drive(63)
        key_file = keyFile

    if newUser is True:  
        init = input("What would you like to do? 'U' = Upload/Update File 'X'=Quit \n ")
    else:
        init = input("What would you like to do? 'U' = Upload/Update File 'D'=Download File 'X'=Quit \n ")

    while init != 'X':
        if init=='U':

            keyFile = input("Where is your key file stored? \n")
            fileName = input("What is the file name? \n")
            oram.write(fileName)
            print("File uploaded successfully \n")
        elif init=="D":
            keyFile = input("Where is your key file stored? \n")
            fileName = input("What is the file name? \n")
            oram.read(fileName)
            print("File downloaded successfully \n")
        init = input("What would you like to do? 'U' = Upload/Update File 'D'=Download File 'X'=Quit \n")



