from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive 
gauth = GoogleAuth() 
drive = GoogleDrive(gauth)


def file_upload(upload_file_list: list[str]) -> None:
    for upload_file in upload_file_list: 
        gfile = drive.CreateFile(None)
        gfile.SetContentFile(upload_file) 
        gfile.Upload()

def file_download(file_name: str) -> None:
    #going to need to access global key, encrypt file_name and use that to get the encrypted file
    file_list = drive.ListFile({'q': f"'root' in parents and trashed=false and title = '{file_name}'"}).GetList() 
    for file in file_list: 
        print('title: %s, id: %s' % (file['title'], file['id']))
    print(file_list)
    for i, file in enumerate(sorted(file_list, key = lambda x: x['title']), start=1): 
        print('Downloading {} file from GDrive ({}/{})'.format(file['title'], i, len(file_list))) 
        file.GetContentFile(file['title'])