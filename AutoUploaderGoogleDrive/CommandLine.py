import os
import httplib2
import base64
import logging
import argparse
import re
import time

from sys import argv

from apiclient import discovery
from apiclient.http import MediaFileUpload
from apiclient.http import HttpRequest as RequestHttp

from AutoUploaderGoogleDrive.auth import Authorize
from AutoUploaderGoogleDrive.settings import *
from AutoUploaderGoogleDrive.temp import *

import rarfile
from rarfile import Error, BadRarFile, NeedFirstVolume

from email.mime.text import MIMEText


class main(object):    
    script, localFolder = argv
    logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s %(message)s')
    def __init__(self, localFolder=None):
        http = Authorize()
        if localFolder:
            self.localFolder = localFolder
        self.serviceGmail = discovery.build('gmail', 'v1', http=http)
        self.serviceDrive = discovery.build('drive', 'v2', http=http)
        self.JSONResponseList = []
        self.Public = True
        self.extractedFilesList = []
        self.nonDefaultPermissions = nonDefaultPermissions
        try:
            logging.debug('Attempting to pull information from daemon env')
            self.bt_name = os.getenv('TR_TORRENT_NAME')
            logging.debug("Pulled bt_name successfully: %s" % self.bt_name)
            self.bt_time = os.getenv('TR_TIME_LOCALTIME')
            logging.debug("Pulled bt_time successfully: %s" % self.bt_time)
            self.bt_app = os.getenv('TR_APP_VERSION')
            logging.debug("Pulled app_version successfully: %s" % self.bt_app)
            self.bt_dir = os.getenv('TR_TORRENT_DIR')
            logging.debug("Pulled Torrent Dir successfully: %s " % self.bt_dir)
            self.bt_hash = os.getenv('TR_TORRENT_HASH')
            logging.debug("Pulled hash successfully: %s " % self.bt_hash)
            self.bt_id = os.getenv('TR_TORRENT_ID')
            logging.debug("Pulled torrent_id successfully: %s" % self.bt_id)
            self.fullFilePaths = os.path.join(self.bt_dir, self.bt_name)
            logging.debug("Joined bt_dir and bt_name to get %s" % self.fullFilePaths)
            self.FilesDict = self.createDirectoryStructure(self.fullFilePaths)
            logging.debug("Creating dictionary of files: %s" % self.FilesDict)
            logging.debug('Information pulled successfully')
        except(AttributeError):
            self.fullFilePaths = self.localFolder
            self.folderName = self.fullFilePaths.rsplit(os.sep)
            logging.debug("Using %s" % self.folderName)
            self.bt_name = self.folderName[-2]
            logging.debug("Using %s" % self.bt_name)
            self.FilesDict = self.createDirectoryStructure(self.fullFilePaths)
        
        logging.debug("Using %s as FilesDict" % self.FilesDict)
        self.autoExtract(self.fullFilePaths)
        self.uploadPreserve(self.FilesDict, Folder_ID=googledrivedir)
        tempfilename = '/var/tmp/transmissiontemp/transmission.%s.%s.html' % (self.bt_name, os.getpid())
        setup_temp_file(tempfilename)
        for EachEntry in self.JSONResponseList:
            addentry(tempfilename, EachEntry)
        finish_html(tempfilename)
        email_subject = ("%s has finished downloading.") % self.bt_name
        email_message = self.encodeMessage(email_subject, tempfilename)
        self.sendMessage(email_message)
        logging.debug("Contents of extractFilesList %s" % self.extractedFilesList)

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
                folders = path[start:].split(os.sep)
                subdir = dict.fromkeys(files, ['None', filepath])
                parent = reduce(dict.get, folders[:-1], dir)
                parent[folders[-1]] = subdir
            except:
                filepath = path
                folders = path[start:].split(os.sep)
                subdir = dict.fromkeys(files, ['None', filepath])
                parent = reduce(dict.get, folders[:-1], dir)
                parent[folders[-1]] = subdir
        return dir

    def autoExtract(self, directory):
        for path, dirs, files in os.walk(directory):
            for EachFile in files:
                filepath = os.path.join(path, EachFile)
                if rarfile.is_rarfile(filepath):
                    logging.debug("UNRAR: Archive %s found." % filepath)
                    try:
                        logging.debug("UNRAR: Attemping extraction....")
                        with rarfile.RarFile(filepath) as rf:
                            startExtraction = time.time()
                            rf.extractall(directory)
                            timeToExtract = time.time() - startExtraction
                            self.extractedFilesList.append(
                                                    {
                                                    'FileList': rf.namelist(),
                                                    'TimeToUnrar': timeToExtract
                                                     }
                                                    )
                            logging.debug("UNRAR: Extraction for %s took %s." % (filepath, timeToExtract))
                    except: 
                        logging.debug("Moving onto next file.")

    def cleanUp(self):
        logging.info("CLEANUP: Cleanup started. Deleting extracted files.")
        DeleteFiles = self.extractedFilesList
        for EachFile in DeleteFiles:
            logging.info("CLEANUP: Deleting %s." % EachFile)
            os.remove(EachFile)
            logging.info("CLEANUP: Deleted %s successfully." % EachFile)
        logging.info("CLEANUP: Cleanup completed.")

    def fetchTorrentFile(self, bt_name):
        """
        Fetches the Torrents file name to parse for sorting.

        Args:
            bt_name: string. Name of the torrent
            
        Returns:
            filepath: /path/to/file to be parsed for trackerinfo
        """
        torrentFileDirectory = self.torrentFileDirectory
        for path, dirs, files in os.walk(torrentFileDirectory):
            for EachTorrent in files:
                if bt_name in EachTorrent:
                    filepath = os.path.join(path, EachTorrent)
                    return filepath 

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
        if parents:
            body['parents'] = [{'id' : parents}]
        response = service.files().insert(body=body).execute()
        if self.nonDefaultPermissions == True:
            fileID = response['id']
            self.setPermissions(fileID)
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
        response = service.users().messages().send(userId='me', body=message).execute()
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
                    refilter = re.compile('.*\\.r.*.*\\Z(?ms)')
                    if refilter.match(fullPathToFile):
                        logging.debug("%s skipped." % fullPathToFile)
                    else:    
                        response = self.uploadToGoogleDrive(fullPathToFile, FF, Folder_ID=Folder_ID)
                        self.JSONResponseList.append(response)
            except(KeyError):
                subfolder = FilesDict[FF]
                subfolder_id = self.createFolder(FF, parents=Folder_ID)
                self.uploadPreserve(subfolder, Folder_ID=subfolder_id)


    def uploadToGoogleDrive(self, FileEntry, FileTitle, Folder_ID=None):
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
        if Folder_ID:
            body['parents'] = [{'id' : Folder_ID}]
        media = MediaFileUpload(FileEntry, chunksize=1024*1024, resumable=True)
        response = service.files().insert(body=body, media_body=media).execute()
        if self.nonDefaultPermissions == True:
            fileID = response['id']
            self.setPermissions(fileID)
        return response

    def setPermissions(self, file_id):
        """
        Sets the permissions for the file
        """
        service = self.serviceDrive
        newPermissions = {
            'value': permissionValue,
            'type': permissionType,
            'role': permissionRole,
            }
        return service.permissions().insert(
            fileId=file_id, body=newPermissions).execute()
           




if __name__ == '__main__':
    script, localFolder = argv
    AutoUploaderGoogleDrive(localFolder)
