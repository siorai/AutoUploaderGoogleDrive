""" Library for uploading functions

"""


from __future__ import print_function
import ConfigParser, os, logging 
from sys import argv

from apiclient import discovery
from AutoUpload.settings import keyfile, client_email, delegated_email #import settings needed to interact with google api


from oauth2client.service_account import ServiceAccountCredentials # service account credentials function

#Pydrive libraries to simplify wrapping and calls of the google API
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#Command arguments to test functionality, should be passed via torrent in future
#script, filename = argv


__author__ = 'siorai@gmail.com (Paul Waldorf)'

logging.basicConfig(filename='/var/tmp/example.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

#variables needed by Google API for auth
scopes = ['https://www.googleapis.com/auth/drive']  

#Instantiates the ServiceAccountCredential object from oauth2client
#from json file given upon ServiceAccount creation via Google Developers Console
#requires the /path/to/json and scopes to be defined.
#json file name cannot be changed as file's encryption is tied to file name.
credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scopes=scopes) #pulled from settings.py

#Method for telling Google Drive's api which user account to access and store files to.
delegated_credentials = credentials.create_delegated(delegated_email) #pulled from settings.py


#Instantiates the GoogleAuth() from pydrive.auth, for use with PyDrive
gauth = GoogleAuth()
#Tells the object to use delegated credentials
gauth.credentials = delegated_credentials

#Instantiates the Drive object from PyDrive
drive = GoogleDrive(gauth)


#Function for uploading filename set in argv when executed
def upload(filename):
    """ Function for sending 'filename' to Google Drive
    
    Args:
      filename: full path/to/file to be uploaded. 
      
    Returns:
      Nothing
    
    """
    filesize = os.path.getsize(filename) # gets file size
    FileTitle = os.path.basename(filename) # removes local directory and returns name of file
    #print('File %s is %s bytes total' % (FileTitle, filesize)) # prints name of file and bytesize
    uploadtext = drive.CreateFile({'title': FileTitle}) # creates file remotely with FileTitle
    uploadtext.SetContentFile(filename) # sets content file
    uploadtext.Upload() # executes upload of content
    print('title: %s, id: %s' % (uploadtext['title'], uploadtext['id'])) #prints title and ID
    permission = uploadtext.InsertPermission({
                                 'type': 'anyone',
                                 'value': 'anyone',
                                 'role': 'reader'}) #sets permissions so anyone can read
 
    print(uploadtext['alternateLink']) #prints link to file
    

    
    
