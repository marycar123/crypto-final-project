
from etoe import decryption, encryption, keygen, enc_name, dec_name
from upload_download import file_upload, file_download
import os


def enc_and_upload(my_file_name: str, key_file_name: str, name_key_file_name: str):
    file = open(my_file_name, "r")
    my_file = file.read()
    my_file = my_file.encode('utf-8')


    keygen(name_key_file_name)
    my_file_name = my_file_name.encode('utf-8')
    encrypted_name = enc_name(my_file_name, name_key_file_name)

    #Key generation, will store key at this file 
    keygen(key_file_name)
    #encrypting file and giving the key store in that file's keyFile
    ct=encryption(my_file, key_file_name, encrypted_name[1])    

    
    combined_name = encrypted_name[0].hex()+encrypted_name[1].hex() + ".txt"
    encrypted_file = open(combined_name, "wb")
    encrypted_file.write(str(ct[0]).encode('utf-8'))
    encrypted_file.write(ct[1])
    encrypted_file.close()

    file_upload([combined_name])
    os.remove(combined_name)

    return ct, my_file, combined_name
    
def download_and_decrypt(download_name, key_file_name, name_key_file_name):

    #downloads the file from google drive
    file_download(download_name)

    #breaks the given file name down to IV and encrypted
    encrypted_bytes_1 = bytes.fromhex(download_name[:32])
    encrypted_bytes_2 = bytes.fromhex(download_name[32:64])
    name_tuple = (encrypted_bytes_1, encrypted_bytes_2)


    #decypt and parse the name to get the original file name
    name_decrypt = dec_name(name_tuple, name_key_file_name)
    name_decrypt = name_decrypt.decode('utf-8')
    name_decrypt = name_decrypt[:(len(my_file_name))]


    #download encrypted contents
    file = open(download_name, "rb")
    ct = file.read()

    #parse the contents for nonce and encryption key for the file
    header = (ct[0:9],encrypted_bytes_2)
    reconstructed_ct =(header, ct[9:])  

    
    #decrypt the file contents
    result = decryption(reconstructed_ct, key_file_name)

    #create a new file under the decrypted name and write the decypted contents to it
    decrypted_file = open(name_decrypt, "w")
    decrypted_file.write(result.decode('utf-8'))
    decrypted_file.close()
    #os.remove(decrypted_file)

    return None


if __name__ == '__main__':
    my_file_name = input("Enter a file Name: ")
    key_file_name = input("Where do you want to store your key? ")
    name_key_file_name = input("Where do you want the name key to be stored? ")
    ct, my_file, combined_name = enc_and_upload(my_file_name, key_file_name, name_key_file_name)
    download_and_decrypt(combined_name,key_file_name,name_key_file_name)

