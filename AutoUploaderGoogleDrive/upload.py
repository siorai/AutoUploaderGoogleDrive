""" Library for uploading functions

"""


from __future__ import print_function
import ConfigParser, os, logging 
from sys import argv

import settings
from apiclient import discovery
from settings import servicekeyfile, client_email, delegated_email, logfile, flow_to_use, scopes  #import settings needed to interact with google api

import auth
from oauth2client.service_account import ServiceAccountCredentials # service account credentials function

#Pydrive libraries to simplify wrapping and calls of the google API
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#Command arguments to test functionality, should be passed via torrent in future
#script, filename = argv


__author__ = 'siorai@gmail.com (Paul Waldorf)'

logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s %(message)s')

#Instantiates the ServiceAccountCredential object from oauth2client
#from json file given upon ServiceAccount creation via Google Developers Console
#requires the /path/to/json and scopes to be defined.
#json file name cannot be changed as file's encryption is tied to file name.
#credentials = ServiceAccountCredentials.from_json_keyfile_name(servicekeyfile, scopes=scopes) #pulled from settings.py

#Method for telling Google Drive's api which user account to access and store files to.
#delegated_credentials = credentials.create_delegated(delegated_email) #pulled from settings.py
#client_email = settings.client_email

#Instantiates the GoogleAuth() from pydrive.auth, for use with PyDrive
#gauth = GoogleAuth()
#Tells the object to use delegated credentials
#gauth.credentials = delegated_credentials

#Instantiates the Drive object from PyDrive
#drive = GoogleDrive(gauth)


#Function for uploading filename set in argv when executed
def upload(FileTitle):
    """ Function for sending 'filename' to Google Drive
    
    Args:
      filename: full path/to/file to be uploaded. 
      
    Returns:
      direct_gdrive_link: the generated link to the file
	that was uploaded
    
    """

    #The following settings are from the PyDrive library and need in order to make the 
    #call to the google drive api and upload the physical files, they will phased out 
    #and replaced with my own ASAP
    credentials = ServiceAccountCredentials.from_json_keyfile_name(servicekeyfile, scopes=scopes)
    delegated_credentials = credentials.create_delegated(delegated_email)
    client_email = settings.client_email
    gauth = GoogleAuth()
    gauth.credentials = delegated_credentials    
    drive = GoogleDrive(gauth)

    #filesize = os.path.getsize(filename) # gets file size
    #FileTitle = os.path.basename(filename) # removes local directory and returns name of file
    #print('File %s is %s bytes total' % (FileTitle, filesize)) # prints name of file and bytesize
    uploadtext = drive.CreateFile({'title': FileTitle}) # creates file remotely with FileTitle
    uploadtext.SetContentFile(FileTitle) # sets content file
    uploadtext.Upload() # executes upload of content
    #print('title: %s, id: %s' % (uploadtext['title'], uploadtext['id'])) #prints title and ID
    #permission = uploadtext.InsertPermission({
    #                            'type': 'anyone',
    #                             'value': 'anyone',
    #                             'role': 'reader'}) #sets permissions so anyone can read
 
    #print(uploadtext['alternateLink']) #prints link to file
    direct_gdrive_link = uploadtext['alternateLink']
    return direct_gdrive_link

    
#upload()   
