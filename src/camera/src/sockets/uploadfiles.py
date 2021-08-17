from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# upload_file_list = ['1.jpg', '2.jpg']

# for upload_file in upload_file_list:
#     gfile = drive.CreateFile(
           
#     )




folder_name = 'test3'
folder = drive.CreateFile({'title' : folder_name, 'mimeType' : 'application/vnd.google-apps.folder'})
folder.Upload()
