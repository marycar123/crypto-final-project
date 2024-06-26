from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive 
gauth = GoogleAuth() 
drive = GoogleDrive(gauth)


def file_upload(upload_file_list: list[str]) -> None:
    file_list = drive.ListFile({'q': f"'root' in parents and trashed=false"}).GetList()
    for upload_file in upload_file_list: 
        for file in file_list:
            if file['title'] == upload_file:
                file.Delete()
                print("delete success")
                break
        gfile = drive.CreateFile(None)
        gfile.SetContentFile(upload_file) 
        gfile.Upload()

def file_download(file_name: str) -> None:
    #going to need to access global key, encrypt file_name and use that to get the encrypted file
    file_list = drive.ListFile({'q': f"'root' in parents and trashed=false and title = '{file_name}'"}).GetList() 
    for i, file in enumerate(sorted(file_list, key = lambda x: x['title']), start=1): 
        print('Downloading {} file from GDrive ({}/{})'.format(file['title'], i, len(file_list))) 
        file.GetContentFile(file['title'])

