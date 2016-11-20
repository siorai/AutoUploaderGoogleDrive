from __future__ import print_function
import httplib2
import ConfigParser, os 
from sys import argv

from httplib2 import Http
from apiclient import discovery

#Imports related to oauth2's authentication flow
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import service_account
from oauth2client.service_account import ServiceAccountCredentials

#Pydrive libraries to simplify wrapping and calls of the google API
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#Command arguments to test functionality, should be passed via torrent in future
script, filename = argv

#Instantiates the config parser object to pull data from settings.ini
config = ConfigParser.RawConfigParser(allow_no_value=False)
config.readfp(open('settings.ini'))


#variables needed by Google API for auth
scopes = ['https://www.googleapis.com/auth/drive'] 
client_email = config.get("credentials", "client_email") #pulled from settings.ini

#Instantiates the ServiceAccountCredential object from oauth2client
#from json file given upon ServiceAccount creation via Google Developers Console
#requires the /path/to/json and scopes to be defined.
#json file name cannot be changed as file's encryption is tied to file name.
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    config.get("credentials", "keyfile"), scopes=scopes) #pulled from settings.ini

#Method for telling Google Drive's api which user account to access and store files to.
delegated_credentials = credentials.create_delegated(config.get("credentials", "delegated_email")) #pulled from settings.ini

http = delegated_credentials.authorize(httplib2.Http())




#Instantiates the GoogleAuth() from pydrive.auth, for use with PyDrive
gauth = GoogleAuth()
#Tells the object to use delegated credentials
gauth.credentials = delegated_credentials

#Instantiates the Drive object from PyDrive
drive = GoogleDrive(gauth)


#Function for calling PyDrive Object to upload to google Drive
#
#Done in 6 steps.
#The first API call creates a file and sets the metadata tag 'title' to match the filename 
#The second points to the actual content file locally.
#the third step uploads the content file to the newly created file on google drive
#The fourth step prints the metadata tags 'title' and 'id' and returns it to the user
#The fifth step changes the permission via the metadata tags 'type' 'value' and 'role'
#to enable 'anyone' 'anyone' 'reader' effectively making the file public to anyone to view
#The sixth step returns the contents of the 'alternateLink' metadata tag to user which provides a link to the user to access that file directly


def main():



    uploadtext = drive.CreateFile({'title': filename}) 
    uploadtext.SetContentFile(filename) 
    uploadtext.Upload()
    print('title: %s, id: %s' % (uploadtext['title'], uploadtext['id']))
    permission = uploadtext.InsertPermission({
                                 'type': 'anyone',
                                 'value': 'anyone',
                                 'role': 'reader'})
 
    print(uploadtext['alternateLink'])
    
if __name__ == '__main__':
    main()
