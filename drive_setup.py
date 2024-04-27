from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive 
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

