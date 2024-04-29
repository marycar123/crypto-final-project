
from etoe import decryption, encryption, keygen
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
    # myFileName = input("Enter a file Name: ")
    # keyFileName = input("Where do you want to store your key? ")
    # nameKeyFileName = input("Where do you want the name key to be stored? ")

    #my_file_name = "test.txt"
    #ct, my_file = enc_and_upload(my_file_name)
    #download_and_decrypt(my_file_name)
    setup_drive(63)

