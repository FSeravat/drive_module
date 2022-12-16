from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class DriveService:

    def __init__(self, driveId):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        self.service = build('drive', 'v3', credentials=creds, static_discovery=False)
        self.driveId = driveId

    def get_file(self, id):
        file = {}
        try:
            response = self.service.files().get(
                fileId=id,
                supportsAllDrives=True,
                fields='id, name,parents, size, createdTime, modifiedTime'
            ).execute()
            file = response
        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file

    def view_all_files(self,folder=""):
        try:
            files = []
            q = "mimeType!='application/vnd.google-apps.folder' and trashed=false"
            if folder!="":
                q+=" and '"+folder+"' in parents"
            page_token = None
            while True:
                response = self.service.files().list(
                                                            q=q,
                                                            driveId=self.driveId,
                                                            corpora="drive",
                                                            fields='nextPageToken, '
                                                                    'files(id, name,parents, size, createdTime, modifiedTime)',
                                                            supportsAllDrives=True,
                                                            includeItemsFromAllDrives=True,
                                                            pageToken=page_token
                                                        ).execute()
                files.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
        except HttpError as error:
            print(F'An error occurred: {error}')
            files = None

        return files
    

    def view_all_folders(self,folder=""):
        try:
            folders = []
            q = "mimeType='application/vnd.google-apps.folder' and trashed=false"
            if folder!="":
                q+=" and '"+folder+"' in parents"
            page_token = None
            while True:
                response = self.service.files().list(
                                                            q=q,
                                                            driveId=self.driveId,
                                                            corpora="drive",
                                                            fields='nextPageToken, '
                                                                    'files(id, name, parents)',
                                                            supportsAllDrives=True,
                                                            includeItemsFromAllDrives=True,
                                                            pageToken=page_token
                                                        ).execute()
                folders.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
        except HttpError as error:
            print(F'An error occurred: {error}')
            folders = None

        return folders