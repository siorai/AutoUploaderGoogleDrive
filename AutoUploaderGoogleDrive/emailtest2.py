#!/usr/bin/env python
from __future__ import print_function
import os
import httplib2
import base64 
from sys import argv

from apiclient import discovery # Interacting with google API
from email.mime.text import MIMEText # For email encoding 
import logging
from apiclient.http import MediaFileUpload
from apiclient.http import HttpRequest as RequestHttp
from AutoUploaderGoogleDrive.auth import Authorize

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from AutoUploaderGoogleDrive.settings import * #import settings needed to interact with googleapi
from upload import upload
import AutoUploaderGoogleDrive.temp
from AutoUploaderGoogleDrive.temp import setup_temp_file, addentry, finish_html

#from oauth2client.service_account import ServiceAccountCredentials #ServiceLevelAccount 
logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s %(message)s') #logging config
#credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scopes=scopes) #ServiceAccount object
#delegated_credentials = credentials.create_delegated(delegated_email) #delegates which users files to access

http = Authorize()
JSONResponseList = []


def main(Folder=None):
    """Sends an email based on hard parameters as specified in encode_message 
    to be changed at a later time with user configurable things.
    
    Returns: Nothing
    """
    http = Authorize()
    service = discovery.build('gmail', 'v1', http=http) #defines the api service
      
    


        
    sender_email = delegated_email # self email, will make this a setting later
    try:
        bt_name = os.getenv('TR_TORRENT_NAME') # fetches torrent name env var
        bt_time = os.getenv('TR_TIME_LOCALTIME')
        bt_app = os.getenv('TR_APP_VERSION')
        bt_dir = os.getenv('TR_TORRENT_DIR', Folder)
        bt_hash = os.getenv('TR_TORRENT_HASH')
        bt_id = os.getenv('TR_TORRENT_ID')
    
    

    
    #pathtofilename = ([bt_dir, bt_name])
        full_file_paths = os.path.join(bt_dir, bt_name)
        FilesDict = getDirectoryStructure(full_file_paths)       
        
    except(AttributeError):

        full_file_paths = Folder
        folderName = full_file_paths.rsplit(os.sep)
        bt_name = folderName[-1]
        FilesDict = getDirectoryStructure(full_file_paths)

    # for EachFile in list_of_files:
    #  logging.info('Starting upload of %s') % EachFile
    #  upload(EachFile)

    uploadPreserve(FilesDict, JSONResponseList, Folder_ID=googledrivedir)
    tempfilename = "/var/tmp/transmissiontemp/transmission.%s.%s.html" % (bt_name, os.getpid())
    setup_temp_file(tempfilename)
    for EachResponse in JSONResponseList:
        addentry(tempfilename, EachResponse)
    finish_html(tempfilename)

    email_subject = ("%s has finished downloading!") % bt_name # will make this a setting to change later as well
    
    #setup_message(list_of_files, bt_time)
    

    
    test_message = encode_message(email_subject, tempfilename) #defines what to use for encode_messag
    sent_test = send_message(service, "me", test_message)
    
    sent_test
    
def encode_message(subject, tempfilename, message_text=None):
    """ Basic MIMEText encoding 
    
    Args:
        sender: email address of the sender
        to: email address of where it's goin'
        subject: da subject of da email
        message_text: da body of da email
    
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

def send_message(service, user_id, message):
    """ Sends da email
    
    Args:
        service: Authorized Google Service Object
        user_id: User's email address. Using "me" can be
        used to indicate the authenticated user
        message: encoded message to be sent
        
    Returns:
        Sent Message.
    """
    
    message = (service.users().messages().send(userId='me', body=message)
		 .execute())
    logging.warning('Email sent')
    return message
   
def get_filepaths(directory):
    """ Function for getting the full filepaths extrapolated from the env
    'TR_TORRENT_NAME' and 'TR_TORRENT_DIR' as passed from transmission
    
    Args: 
        directory: directory containing files to be uploaded
        
    Returns:
        file_paths: A list containing path names for all of the files to be uploaded

     """

    file_paths = []

    for root, directories, files in os.walk(directory):
      for filename in files:
          filepath = os.path.join(root, filename)
          file_paths.append(filepath)
    return file_paths


def uploadPreserve(FilesDict, JSONResponse, Folder_ID=None):
    for FF in FilesDict:
        i = FilesDict[FF]
        try:
            if i[0]:
                Full_Path_To_File = os.path.join(i[1], FF)
                response = uploadToGoogleDrive(Full_Path_To_File, FF, Folder_ID=Folder_ID)
                JSONResponse.append(response)
        except(KeyError):
            #print("Folder found! Created %s") % i
            subfolder = FilesDict[FF]
            subfolder_id = createFolder(FF, parents=Folder_ID)
            uploadPreserve(subfolder, JSONResponse, Folder_ID=subfolder_id)
        


def getDirectoryStructure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
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




'''
def setup_message2(FilesDict, bt_time, bt_name, Master_Folder_ID=None):
    """ Sets up message preserving file structure

    """
    http = Authorize()
    tempfilename = '/var/tmp/transmissiontemp/transmission.%s.%s.html' % (bt_name,os.getpid())
    setup_temp_file(tempfilename)
    Folder_ID = createFolder(bt_name, parents=Master_Folder_ID)
    JSONResponse = []
    uploadPreserve(FilesDict, JSONResponse, Folder_ID=Folder_ID)
    for EachUpload in JSONResponse:
'''            



'''
def setup_message(list_of_files, bt_time, bt_name, Master_Folder_ID=None):
    """ Setup creation of email text body
   
    Args:
	list_of_files: the list of files to be sent
	time_uploaded: time string returned from os.getenv('TR_TIME_LOCALTIME')
	
    Returns:
	tempfilename as a string
    """
    http = Authorize() 
    logging.debug('TEMP: TempFile initializing') 
    tempfilename = '/var/tmp/transmissiontemp/transmission.%s.html' % os.getpid()
    logging.debug('TEMP: TempFile pathname set to %s' % tempfilename)
    setup_temp_file(tempfilename)
    Folder_ID = createFolder(bt_name, parents=Master_Folder_ID)
'''
""" 
    for EachEntry in list_of_files:
        #if os.path.isdir(EachEntry) == True:
        #    DirName = os.path.split(EachEntry)
        #    createFolder(DirName, parents=Folder_ID)
        FileSize = os.path.getsize(EachEntry)
        logging.debug('TEMP: Setting filesize for %s to %s' % (EachEntry, FileSize))
        FileTitle = os.path.basename(EachEntry)
        logging.debug('TEMP: Setting FileTitle for %s to %s' % (EachEntry, FileTitle))
        responsejson = uploadToGoogleDrive(EachEntry, FileTitle, Folder_ID=Folder_ID)
        direct_gdrive_link = responsejson['webContentLink']
        createdDate = responsejson['createdDate']
        print(responsejson)
      
        addentry(tempfilename, createdDate, FileSize, FileTitle, direct_gdrive_link)
    finish_html(tempfilename)
    
    return tempfilename
"""

def uploadToGoogleDrive(EachEntry, FileTitle, Folder_ID=None, Public=None):
    http = Authorize()
    drive_api = discovery.build('drive', 'v2', http=http)
    #logging.debug('UPLOADER: Uploading %s to GoogleDrive.') % EachEntry
    body = {
            'title': FileTitle
        }
    if Folder_ID:
        body['parents'] = [{'id' : Folder_ID}]
    media = MediaFileUpload(EachEntry, chunksize=1024*1024, resumable=True)
    response = drive_api.files().insert(body=body, media_body=media).execute()
    return response

def createFolder(bt_name, parents=None):
    http = Authorize()
    drive_api = discovery.build('drive', 'v2', http=http)
        
    file_metadata = {
        'title' : bt_name,
        'mimeType' : 'application/vnd.google-apps.folder'
    }
    if parents:
        file_metadata['parents'] = [{'id': parents}]
    folder = drive_api.files().insert(body=file_metadata).execute()
    print(folder)
    return folder['id']
    

def getIDs():
    http = Authorize()
    drive_api = discovery.build('drive', 'v2', http=http)
    IDs = drive_api.files().generateIds().execute()
    return IDs['ids']
            

if __name__ == '__main__':
    script, Folder = argv
    main(Folder)
    

