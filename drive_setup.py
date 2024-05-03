from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive 
from upload_download import file_upload
from etoe import encryption, keygen
import os

gauth = GoogleAuth() 
drive = GoogleDrive(gauth)

def drive_wipe() -> None:
    #get all files in the root directory, no folders pls
    file_list = drive.ListFile({'q': f"'root' in parents and trashed=false"}).GetList()

    # for every file try to delete it
    for i, file in enumerate(sorted(file_list, key=lambda x: x['title']), start=1):
        try:
            file.Delete()  
            print('File {} deleted from Google Drive.'.format(file['title'])) #print in terminal which file deleted
        except Exception as e:
            print('An error occurred while deleting the file:', e)

def dummy_data_upload(num_Files: int, key_File_Name) -> None:
    file_Names: list[str] = []
    for i in range(0,num_Files):
        file: str = f"File_{i}.txt"
        dummy: str = "0" * (2**16)
        dummy_nonce, dummy_encrypted = encryption(dummy.encode("utf-8"), key_File_Name)
        local_file = open(file, "wb")
        local_file.write(str(dummy_nonce).encode('utf-8'))
        local_file.write(dummy_encrypted)
        local_file.close()
        file_Names.append(file)
        print(f"{local_file} created")
    file_upload(file_Names)
    print("upload finished")
    for name in file_Names:
        os.remove(name)
    return

