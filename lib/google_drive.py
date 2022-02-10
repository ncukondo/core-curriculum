import os.path
import mimetypes
import os
import io
import enum

from google_auth import get_creds
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http

''' 
requirements
google-api-python-client 
google-auth-httplib2 
google-auth-oauthlib 
'''

'''
save client secrets(as InstalledApp) in 'client_secrets.json'
'''

class FileExtType(enum.Enum):
    """ class for enum file extention to export"""
    XLSX = "xlsx"
    DOCX = "docx"
    PDF = "pdf"
    HTML = "html"


API_SERVICE_NAME = "drive"
API_VERSION = "v3"
CLIENT_SECRETS_FILE =  os.path.join(os.path.dirname(__file__),'client_secrets.json')
CLIENT_TOKEN =  os.path.join(os.path.dirname(__file__),'token.json')
SCOPES = ['https://www.googleapis.com/auth/drive']

def from_service_account():
    """ make GoogleDrive instance from service account information """
    return GoogleDrive(get_creds())

class GoogleDrive:
    ''' class of thin wrapper for googleapiclient '''

    def __init__(self,cred:Credentials):
        self.cred=cred
        self.service = build(API_SERVICE_NAME, API_VERSION, http=cred.authorize(Http()))

    def upload(self,file:str,parent_id:str)->str:
        """ upload local file to drive """
        file_metadata = {
            'name': os.path.basename(file),
            'parents': [parent_id]
        }
        media = MediaFileUpload(
            file, 
            mimetype=mimetypes.guess_type(file)[0], 
            resumable=True
        )
        drive_file = self.service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        return drive_file.get("id")

    def download(self,file_id:str,dest_path:str=".")->bool:
        """ download content from drive """
        file=self.service.files().get(
            fileId=file_id,
            supportsAllDrives=True).execute()
        path = os.path.join(dest_path,file["name"])
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(path, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        return done

    def export(self,file_id:str,file_type:FileExtType,dest_path:str=".")->bool:
        """ export google doc/sheet from drive """
        file=self.service.files().get(
            fileId=file_id,
            supportsAllDrives=True).execute()
        ext = str(file_type)
        mime_type= mimetypes.guess_type(f"sample.{ext}")[0]
        path = os.path.join(dest_path,file["name"]+"."+ext)
        request = self.service.files().export_media(
            fileId=file_id,
            mimeType=mime_type)
        fh = io.FileIO(path, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        return done



def main():
    print(mimetypes.guess_type("sample.xlsx")[0])
    from_service_account().export(
        "1Dg2QAub4L0Hjxoby-tl3REQSMk8AvKt4h2_UVbufVvc",FileExtType.xlsx)

if __name__ == '__main__':
    main()
