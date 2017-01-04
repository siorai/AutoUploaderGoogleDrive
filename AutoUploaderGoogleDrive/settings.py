import logging
import httplib2
import os
"""
Settings script containing all account related variables
and customization options as they are become created
through development.

Variables for scopes, logfile are required for any one 
of the three oauth2 flows to function correctly.

flow_to_use variable must be set to either 
"ServiceAccountFlow"
"Oauth2JSONFlow"
"Oauth2WebFlow"

For the purposes of early testing the functionality of
all three of these auth flow types, AutoUploaderGoogleDrive.emailtest
will import all types for right now but will use the one 
indicated by 'flow_to_use'
"""

__author__ = 'siorai@gmail.com (Paul Waldorf)'
#########################
#[Transmission settings]#
#########################

torrentFileDirectory = "/path/to/torrent/directory/"

###########################
#[Remote sorting settings]#
###########################

categoriesDictSettings = {
    'Music': { 
        'Folder_ID': ['somefolder'],
        'Matches': {
            'Match_Tracker': ['sometracker']                          ],
            'Match_Content_Extention' : [ 
                    '*.aac', 
                    '*.flac', 
                    '*.mp3'
            ]
        }
    },
    'TV':   {
        'Folder_ID': ['somefolder'],
        'Matches': {
            'Match_Tracker': ['sometracker'],
            'Match_Expression': [
                '*.S??E??.*', 
                '*.s??e??.*'
            ]

        }
    },
    'Movies':{
        'Folder_ID': ['somefolder'],
        'Matches': {
            'Match_Tracker': ['sometracker']
        }
    },
    'XXX': {  
        'Folder_ID': ['somefolder'],
        'Matches': {
            'Match_Tracker' : ['sometracker']
        }
    }
}


###################
#[Shared settings]#
###################

flow_to_use = "Oauth2JSONFlow" 
# choices are:
# "ServiceAccountFlow" ( Implemented )  
# "Oauth2JSONFlow" ( Implemented )
# "Oauth2WebFlow" ( Not Implemented ) 

scopes =    [
                'https://www.googleapis.com/auth/drive', 
                'https://www.googleapis.com/auth/gmail.compose',
                'https://www.googleapis.com/auth/urlshortener'
            ]
redirect_uri = "http://example.com/auth_return"
googledrivedir = ['defaultgoogledrivedirhere']

####################
#[Logging settings]#
####################

logfile = "/path/to/log/file.log"
loggingSetup = logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s %(message)s')
httplib2.debuglevel = 4


################################
#[Google Drive Upload Settings]#
################################

nonDefaultPermissions = True
permissionValue = 'anyone'
permissionType = 'anyone'
permissionRole = 'reader'

chunksize = 50000*1024 #Uploading Chunksize


##################
#[Email settings]#
##################

emailparameters = ['title', 'md5Checksum', 'id', 'alt_tiny', 'fileSize']
emailSender = "some@email.com"
emailTo = "some@email.com"
deleteTmpHTML = False
tempfilename = '/path/to/temp/html/file.html' % os.getpid()

###############################
#[Service Account Credentials]#
###############################

servicekeyfile = "/path/to/servicekey.json"
client_email = "someprojectname@blahblah.gserviceaccount.com"
delegated_email = "userdata@access.com"

############################
#[Normal JSON Oauth2 Creds]#
############################

pickledcredsFile = "/path/to/pickledcredsFile"
oauth2keyfile = "/path/to/oauth2key.json"
redirect_uri = 'urn:ietf:wg:oauth:2.0:oob' 

#################################
#[Normal WebServer Oauth2 Creds]#
#################################

oauth2web_id = "randomintblahblah.apps.googleusercontent.com"
oauth2web_secret = "oauth2web_secret"
