from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive 
from upload_download import file_upload
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

def dummy_data_upload(num_Files: int) -> None:
    file_Names: list[str] = []
    for i in range(0,num_Files):
        file: str = f"File_{i}.txt"
        local_file = open(file, "w")
        local_file.write(f"test{i}")
        local_file.close()
        file_Names.append(file)
    file_upload(file_Names)
    for name in file_Names:
        os.remove(name)

dummy_data_upload(10)

