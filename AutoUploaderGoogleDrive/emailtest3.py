import os
import httplib2
import base64
import logging

from sys import argv

from apiclient import discovery
from apiclient.http import MediaFileUpload
from apiclient.http import HttpRequest as RequestHttp

from AutoUploaderGoogleDrive.auth import Authorize
#from AutoUploaderGoogleDrive.temp import setup_temp_file, addentry, finish_html
from AutoUploaderGoogleDrive.settings import *


from email.mime.text import MIMEText


class AutoUploaderGoogleDrive(object):
    

    def __init__(self, localFolder=None):
        http = Authorize()
        self.serviceGmail = discovery.build('gmail', 'v1', http=http)
        self.serviceDrive = discovery.build('drive', 'v2', http=http)
        self.JSONResponseList = []
        try:
            self.bt_name = os.getenv('TR_TORRENT_NAME')
            self.bt_time = os.getenv('TR_TIME_LOCALTIME')
            self.bt_app = os.getenv('TR_APP_VERSION')
            self.bt_dir = os.getenv('TR_TORRENT_DIR', localFolder)
            self.bt_hash = os.getenv('TR_TORRENT_HASH')
            self.bt_id = os.getenv('TR_TORRENT_ID')
            self.fullFilePaths = os.path.join(bt_dir, bt_name)
            self.FilesDict = self.getDirectoryStructure(self.fullFilePaths)
        except(AttributeError):
            self.fullFilePaths = localFolder
            self.folderName = self.fullFilePaths.rsplit(os.sep)
            self.bt_name = folderName[-1]
            self.FilesDict = createDirectoryStructure(self.fullFilePaths)
    


    def createDirectoryStructure(self, rootdir):
        """
        Creates dictionary using os.walk to be used for keeping track
        of the local torrent's file structure to recreate it on Google Drive
        Any folders it finds, it creates a new subdictionary inside, however 
        when it locates files adds a list to each entry the first of which is 'File'
        and the second of which is the full path/to/file to be used by
        self.uploadToGoogleDrive.

        Args:
            rootdir: string. path/to/directory to be recreated.

        Returns:
            dir: dictionary. Dictionary containing directory file structure and
                full paths to file names
        """
        dir = {}
        rootdir = rootdir.rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1
        for path, dirs, files in os.walk(rootdir):
            try:
                filepath = os.path.join(path, files)
                folders = path.[start:].split(os.sep)
                subdir = dict.fromkeys(files, ['File', filepath])
                parent = reduce(dict.get, folders[:-1], dir)
                parent[folders[-1]] = subdir
            except:
                filepath = path
                folders = path[start:1].split(os.sep)
                subdir = dict.fromkeys(files, ['File', filepath])
                parent = reduce(dict.get, folders[:-1], dir)
                parent[folders[-1]] = subdir
        return dir

    def getIDs(self):
        service = self.serviceDrive
        IDs = service.files().generateIds().execute()
        return IDs['ids']


    def createFolder(self, folderName, parents=None):
        """
        Creates folder on Google Drive.

        Args:
            folderName: string.  Name of folder to be created
            parents: Unique ID where folder is to be put inside of

        Returns:
            id: unique folder ID 
        """

        service = self.serviceDrive
        body = {'title': folderName,
                'mimeType' : 'application/vnd.google-apps.folder'
        }
        if self.Public == True:
            body['permissions'] = {
                            'type': 'anyone',
                            'value': 'anyone',
                            'role': 'reader'
            }
        if parents:
            body['parents'] = [{'id' : parents}]
        response = service.files().insert(body=body).execute()
        return response['id']

    def encodeMessage(self, subject, tempfilename, message_text=None):
        """
        Basic MIMEText encoding

        Args:
            subject: string. Subject of email
            tempfilename: string. HTML Table create from temp.py
            message_text: string. optional email text in addition to 
                supplied HTML table    
        Returns:
            A base64url encoded email object.
        """    
        readhtml = open(tempfilename, 'r')
        html = readhtml.read()
        message = MIMEText(html, 'html')
        message['to'] = emailTo
        message['from'] = emailSender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def sendMessage(self, message):
        """
        Sends message encoded by encodeMessage.

        Args:
            message: base64url encoded email object.

        Returns:
            JSON response from google.
        """
        service = self.serviceGmail
        response = service.users().messages().send(userId='me', body=message)
            .execute()
        return response

    def uploadPreserve(self, FilesDict, Folder_ID=None):
        """
        Uploads files in FilesDict preserving the local file structure
        as shown by FilesDict created from getDirectoryStructure.
        Appends each JSON response from google return as JSON Data into 
        self.JSONResponse list.

        Args:
            FilesDict: dict. Dictionary representation of files and structure 
                to be created on google drive
            Folder_ID: string. Unique resource ID for folder to be uploaded to.

        Returns:
            Nothing
        """
        for FF in FilesDict:
            i = FilesDict[FF]
            try:
                if i[0]:
                    fullPathToFile = os.path.join(i[1], FF)
                    response = uploadToGoogleDrive(fullPathToTFile,
                                    FF, Folder_ID=Folder_ID)
                    self.JSONResponseList.append(response)
            except(KeyError):
                subfolder = FilesDict[FF]
                subfolder_id = createFolder(FF, parents=Folder_ID)
                uploadPreserve(subfolder, Folder_ID=subfolder_id)


    def uploadToGoogleDrive(self, FilePath, FileTitle, Folder_ID=None):
        """
        Performs upload to Google Drive. 

        Args:
            FilePath: string. Path/To/File/
            FileTitle: string. Passed to the body as the name of the file.
            Folder_ID: string. Unique Folder_ID as assigned by Google Drive.

        Returns:        
            Response in the form of JSON data from Google's REST.

        """

        service = self.serviceDrive
        body = {
                'title': FileTitle
        }
        if self.Public == True: 
            body['permissions'] = {
                        'type': 'anyone',
                        'value': 'anyone',
                        'role': 'reader'
        }
        if Folder_ID:
            body['parents'] = [{'id' : Folder_ID}]
        media = MediaFileUpload(EachEntry, chunksize=1024*1024, resumable=True)
        response = service.files().insert(body=body, media_body=media.execute()
        return response



if __name__ == '__main__':
    print(AutoUploaderGoogleDrive())
