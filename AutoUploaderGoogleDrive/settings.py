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


######################################################
#[General Information and initial setup requirements]#
######################################################
#
# Setting up this script requires a bit of work to setup initially fair warning
# First, you'll need to create your own project at Google at
#
# https://console.developers.google.com
#
# From here, you'll select 'Project' and select create new. Give it a name. 
# Next on the left, you'll need to create some credentials by selecting
# 'Credentials' on the side bar. 
#
# Go over to the OAuth consent screen and select a Product Name, which is
# what you'll see when you authorize this project's ability to access your 
# Google Account.
#
# Then you'll select Credentials.
#
# Here you have two options, an OAuth Client ID, or a Service Account.
#
# OAuth Client ID's are the typical choice for most applications that access
# google services. Typically, most applications that are developed 
# that with any of Google's APIs are usually accessing different users data. 
#
# You can find more about about the OAuth2 standard that google uses over at 
#
# http://developers.google.com/identity/protocols/OAuth2
#
# Service Accounts eliminate the need for any sort of interaction on the 
# user past initial setup which is why it's ideal in this situation.
# However it requires you to have administrative access to your own G-Suite.
# See details below.
#
#  =OAuth2 Client ID Setup=
#
# Select Create Credentials then OAuth2 Cliend ID. When asked for
# the Application type, select 'other', give it a name, and hit create. 
# It'll show your client ID and client secret on screen, don't worry that
# and hit OK. From there you'll see a table with an entry. On the far right
# of that you'll see a download arrow, this is the authentication for 
# your application that identifies the script as being associated with this
# project. Inside this JSON you'll have half of the puzzle to make calls 
# to the API. Rename this file to something more manageable and make
# sure to put it in a location that both your normal user, and the user
# your transmission-daemon runs under can access. (To check to make sure 
# it can access at it, run a 'cat' command against it with a -u (transmission
# user name) argument on it, the same goes for the rest of the script. 
# Keep this file in a secure location, then go down to 
#
# oauth2keyfile = "/path/to/keyfile"
#
# and change it to the path where it can find it. 
#
# oauth2keyfile = "/home/user/json/client_secret.json" 
#
#  =Service Account Setup=
#
# Select create credentials then hit Service Account. Under the Service
# Account drop box, select New Service Account. Make up a name for the
# account, under 'Role', select Project, then Owner. Make sure JSON is ticked
# and not P12. Then create. This will create a copy and then start the 
# download of the only JSON keyfile that will ever be created for this
# service account. If something happens to it, you can't request another 
# copy. (You can just create a new service account using the same process 
# though).
#
# Back on the Credentials page, select 'Manage service accounts' just over the 
# list of Service Account Keys. Here it should show 2 accounts by default, 
# a Compute Engine default service account, and then the one you just created. 
# all the way to the left, you'll see 3 option dots, select that, then check the
# Enable G Suite Domain-wide Delegation box, then save. This will show a new
# option for View Client ID. Selecting that will bring you to a page with the
# client ID that was created for that service account. That ID is what you'll 
# enter into the Administration Console of your G-Suite that authorizes access
# blanket total access to every user under that G-Suite. By utilizing this, 
# you'll also have to select a user name and enter it in 'delegated_email'.
# Since Service Accounts aren't covered under any of the controls normally 
# associated with all accounts on the G-Suite, and thus don't have their own
# assigned spaces for things like Google Drive and Gmail, the 'delegated_email'
# is the user that the service account will access. See
#
# https://developers.google.com/identity/protocols/OAuth2ServiceAccount?hl=en_US#delegatingauthority
#
# for further information.
#
# And fill out the fields under the Service Account Section below. 
#
# =API Activation=
#
# This script currently uses 3 APIs that you'll need to enable on the project
# you've just created. Selecting 'Library' on the left sidebar should load a 
# list of APIs. The three APIs you'll need to enable are the Drive API, the 
# Gmail API, and the URL Shortener API. Select Each one, then up above the 
# description it'll show a button for 'Enable'. Select it. Then go back to 
# the library and enable the other two APIs. 



#########################
#[Transmission settings]#
#########################

torrentFileDirectory = "/path/to/torrent/directory/"

# Local torrent directory where torrents are kept.
# Used to fetch information for parsing tracker details 
# in order to sort.

###########################
#[Remote sorting settings]#
###########################

# Dictionary used for sorting. 
#
# For each catagory listed, you'll need to have a Folder ID 
# that can be obtained from the address when you visit that directory
# remotely on drive.google.com 
#
# For every catagory, there is also a set of rules in place for them 
# Currently these are my working settings and they seem to be working pretty 
# well for my usage. You can get more details on it in the Rules.py script.
#
# Each catagory also has ['Matches']['Match_Tracker'] this will also need to
# be supplied with the relative trackers for each associated catagory.
#
# If you'd rather not mess with the sorting at all and/or run into issues 
# keep this setting as False and it won't run the sorting portion of the 
# script at all.


SortTorrents = False

categoriesDictSettings = {
    'Music': { 
        'Folder_ID': ['somefolder'],
        'Matches': {
            'Match_Tracker': ['sometracker']
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

# This script supports 2 flows currently, one from Service Level Authentication, 
# The other one being Oauth2JSONFlow. 

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



######################################
#[Default Google Drive Upload Folder]#
######################################

# This is the ID of the folder that all uploads will be uploaded to.
# You need to obtain from visiting drive.google.com and entering/creating
# a folder, and taking the 28 character string at the end.
#
# for example: https://drive.google.com/drive/u/3/folders/60B4jmMf2bD9-bm9XSkw2Z2w0d2M
# 
# Would be:
googledrivedir = ['60B4jmMf2bD9-bm9XSkw2Z2w0d2M']

####################
#[Logging settings]#
####################

# Location of logfile.  

logfile = "./upload.log"

# Logging is defaulted for DEBUG for now. Fair warning, this -will- create a rather large
# log. Uploading folders of 2~ gigs have produced log files of over 1MB. Be advised.
# And feel free to adjust accordingly. 

loglevel = logging.DEBUG

loggingSetup = logging.basicConfig(filename=logfile,level=loglevel,format='%(asctime)s %(message)s')

# Setting to include the most possible information from each HTTP request. Defaulted to 4 for 
# troubleshooting

httplib2.debuglevel = 4


################################
#[Google Drive Upload Settings]#
################################

# When set to True, modifies the permisisons of any file/folder created by this script to 
# be viewable by anyone. Change to False to leave it as default.

nonDefaultPermissions = True
permissionValue = 'anyone'
permissionType = 'anyone'
permissionRole = 'reader'

chunksize = 50000*1024 #Uploading Chunksize


##################
#[Email settings]#
##################

# The script will parse the JSON response from the server after each request 
# in order to fill out the data on the table from the email. Visit:
#
# https://developers.google.com/drive/v2/reference/files#resource
#
# For a full list of supported properties.
#
# Note that the 'alt_tiny' is a custom created url that takes the 
# 'alternateLink' property and sends it to the URLShortener API to trim 
# those 50-80 character long links to a more managable size. 

emailparameters = ['title', 'md5Checksum', 'id', 'alt_tiny', 'fileSize']

# Email parameters for the table that gets emailed. Replace both with your
# email associated with google account your using to send it to yourself.

emailSender = "someuser@gmail.com"
emailTo = "someuser@gmail.com"

# When I impliment it, setting this value to True will delete the temporary
# HTML file it creates for the table.

deleteTmpHTML = False

# Temporary file name. os.getpid() (mostly) ensures that tmp files will be
# Unique and not overwritten.

tempfilename = './temp.%s.html' % os.getpid()

###############################
#[Service Account Credentials]#
###############################

servicekeyfile = "/path/to/servicekey.json"
client_email = "someprojectname@blahblah.gserviceaccount.com"
delegated_email = "userdata@access.com"

############################
#[Normal JSON Oauth2 Creds]#
############################

# picklecredsFile location is where the authorized credentials instance will be stored
# for later use. 

pickledcredsFile = "./user.creds"
oauth2keyfile = "/home/someone/client_secret.json"

redirect_uri = 'urn:ietf:wg:oauth:2.0:oob' 

#################################
#[Normal WebServer Oauth2 Creds]#
#################################

# not implimented yet

oauth2web_id = "randomintblahblah.apps.googleusercontent.com"
oauth2web_secret = "oauth2web_secret"
