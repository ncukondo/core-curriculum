""" really thin wrapper for google drive python api client

requirements
google-api-python-client
google-auth-httplib2
google-auth-oauthlib

"""
import os
import os.path
import mimetypes
import io
import enum

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http

from lib.google_auth import get_creds


class FileExtType(enum.Enum):
    """ class for enum file extention to export"""
    XLSX = "xlsx"
    DOCX = "docx"
    PDF = "pdf"
    HTML = "html"

class FileFieldType(enum.Enum):
    """ class represents Fields when getting file """
    KIND="kind"
    ID="id"
    NAME="name"
    MIMETYPE="mimeType"
    DESCRIPTION="description"
    STARRED="starred"
    TRASHED="trashed"
    EXPLICITLYTRASHED="explicitlyTrashed"
    TRASHINGUSER="trashingUser"
    TRASHEDTIME="trashedTime"
    PARENTS="parents"
    PROPERTIES="properties"
    APPPROPERTIES="appProperties"
    SPACES="spaces"
    VERSION="version"
    WEBCONTENTLINK="webContentLink"
    WEBVIEWLINK="webViewLink"
    ICONLINK="iconLink"
    HASTHUMBNAIL="hasThumbnail"
    THUMBNAILLINK="thumbnailLink"
    THUMBNAILVERSION="thumbnailVersion"
    VIEWEDBYME="viewedByMe"
    VIEWEDBYMETIME="viewedByMeTime"
    CREATEDTIME="createdTime"
    MODIFIEDTIME="modifiedTime"
    MODIFIEDBYMETIME="modifiedByMeTime"
    MODIFIEDBYME="modifiedByMe"
    SHAREDWITHMETIME="sharedWithMeTime"
    SHARINGUSER="sharingUser"
    OWNERS="owners"
    TEAMDRIVEID="teamDriveId"
    DRIVEID="driveId"
    LASTMODIFYINGUSER="lastModifyingUser"
    SHARED="shared"
    OWNEDBYME="ownedByMe"
    CAPABILITIES="capabilities"
    VIEWERSCANCOPYCONTENT="viewersCanCopyContent"
    COPYREQUIRESWRITERPERMISSION="copyRequiresWriterPermission"
    WRITERSCANSHARE="writersCanShare"
    PERMISSIONS="permissions"
    PERMISSIONIDS="permissionIds"
    HASAUGMENTEDPERMISSIONS="hasAugmentedPermissions"
    FOLDERCOLORRGB="folderColorRgb"
    ORIGINALFILENAME="originalFilename"
    FULLFILEEXTENSION="fullFileExtension"
    FILEEXTENSION="fileExtension"
    MD5CHECKSUM="md5Checksum"
    SIZE="size"
    QUOTABYTESUSED="quotaBytesUsed"
    HEADREVISIONID="headRevisionId"
    CONTENTHINTS="contentHints"
    INDEXABLETEXT="indexableText"
    IMAGEMEDIAMETADATA="imageMediaMetadata"
    VIDEOMEDIAMETADATA="videoMediaMetadata"
    ISAPPAUTHORIZED="isAppAuthorized"
    EXPORTLINKS="exportLinks"
    SHORTCUTDETAILS="shortcutDetails"
    CONTENTRESTRICTIONS="contentRestrictions"
    RESOURCEKEY="resourceKey"
    LINKSHAREMETADATA="linkShareMetadata"



API_SERVICE_NAME = "drive"
API_VERSION = "v3"
CLIENT_SECRETS_FILE =  os.path.join(os.path.dirname(__file__),'client_secrets.json')
CLIENT_TOKEN =  os.path.join(os.path.dirname(__file__),'token.json')
SCOPES = ['https://www.googleapis.com/auth/drive']

def from_service_account():
    """ make GoogleDrive instance from service account information """
    return GoogleDrive(get_creds())

def make_metadata(local_path:str,parent_id:str=None):
    """ make metadata for google drive """
    file_metadata={'name': os.path.basename(local_path)}
    if parent_id:
        file_metadata["parents"]=[parent_id]
    return file_metadata

def make_mediabody(local_path:str):
    """ make media body for google drive """
    return MediaFileUpload(
            local_path,
            mimetype=mimetypes.guess_type(local_path)[0],
            resumable=True
        )

class GoogleDrive:
    ''' class of thin wrapper for googleapiclient '''

    def __init__(self,cred:Credentials):
        self.cred=cred
        self.service = build(API_SERVICE_NAME, API_VERSION, http=cred.authorize(Http()))

    def upload(self,local_path:str,parent_id:str)->str:
        """ upload local file to drive """
        file_metadata = make_metadata(local_path,parent_id)
        media = make_mediabody(local_path)
        drive_file = self.service.files().create(
            body=file_metadata, media_body=media, fields='id',
            supportsAllDrives=True,
        ).execute()
        return drive_file.get("id")

    def update(self,local_path:str,target_id:str):
        """ update file of the id or upload file """
        file_metadata = make_metadata(local_path)
        media = make_mediabody(local_path)
        drive_file = self.service.files().update(
            body=file_metadata, media_body=media, fileId=target_id,fields='id',
            supportsAllDrives=True,
        ).execute()
        return drive_file.get("id")

    def get_id_by_name(self,name:str,parent_id:str):
        """ get id of the named file in parent_id """
        file_id=''
        file_list = self.get_list(f"'{parent_id}' in parents and name = '{name}'")
        for file in file_list:
            file_id=file["id"]
            break
        return file_id

    def update_by_name(self,local_path:str,parent_id:str):
        """ update file of same name or upload file """
        name = os.path.basename(local_path)
        file_id=self.get_id_by_name(name,parent_id)
        if file_id=='':
            return self.upload(local_path,parent_id)
        return self.update(local_path,file_id)

    def download(self,file_id:str,dest_path:str=".")->str:
        """ download content from drive """
        file=self.service.files().get(
            fileId=file_id,
            supportsAllDrives=True).execute()
        path = os.path.join(dest_path,file["name"])
        request = self.service.files().get_media(fileId=file_id)
        file_handle = io.FileIO(path, mode='wb')
        downloader = MediaIoBaseDownload(file_handle, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        return path

    def export(self,file_id:str,file_type:FileExtType,dest_path:str=".")->str:
        """ export google doc/sheet from drive """
        file=self.service.files().get(
            fileId=file_id,
            supportsAllDrives=True).execute()
        ext = str(file_type).lower()
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
        return path

    def file_info(self,file_id:str,fields:list[FileFieldType]=None):
        """ get file info from drive """
        if fields is None:
            fields=["id","name"]
        return self.service.files().get(
            fileId=file_id,
            fields=",".join(fields),
            supportsAllDrives=True).execute()

    def get_list(self,query:str,fields:list[FileFieldType]=None):
        """ list files in folder """
        if fields is None:
            fields=["id","name","modifiedTime","parents"]
        page_token = None
        while True:
            response = self.service.files().list(
                spaces='drive',
                corpora="user",
                q=query,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageSize=50,
                fields=f'nextPageToken, files({",".join(fields)})',
                pageToken=page_token
            ).execute()
            for file in response.get('files', []):
                yield file
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break


    def list_in_folder(self,folder_id:str,fields:list[FileFieldType]=None):
        """ list files in folder """
        query = f"'{folder_id}' in parents"
        return self.get_list(query,fields)


def main():
    """ for test  """
    print(mimetypes.guess_type("sample.xlsx")[0])
    file_list=from_service_account().list_in_folder(
        "1NrjWTGweLNoUU1n-EH9yhIU5ZBUHOLs1",
        ["id","name","modifiedTime","parents"])
    for file in file_list:
        print(file)
    info = from_service_account().file_info(
        "1UmKJiKjrNjweJFSRg_cpqOw3SbWrdH5VHhja9AR_rtc",
        ["name","modifiedTime","parents"]
        )
    print(info)
    #from_service_account().export(
    #    "1Dg2QAub4L0Hjxoby-tl3REQSMk8AvKt4h2_UVbufVvc",FileExtType.XLSX)

if __name__ == '__main__':
    main()
