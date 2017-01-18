import os
import json
import pprint
import logging

from oauth2client.clientsecrets import InvalidClientSecretsError

from AutoUploaderGoogleDrive.auth import *


logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
logging.basicConfig(filename="setupUploader.log",level=logging.DEBUG,format='%(asctime)s %(message)s')

console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)


logging.getLogger('').addHandler(console)

with open('settings.json', 'rb') as SJ:
    settings = json.load(SJ)

def printSettings(setting=None):
    if setting:
        print("settings.json entry for %s is currently set to %s" % (setting, settings[setting]))
    else:
        for EachSetting in dict.fromkeys(settings):
            print("%s - %s" % (EachSetting, settings[EachSetting]))

def authDriveTest():
    http = Authorize()
    service = discovery.build('drive', 'v2', http=http)
    results = service.files().list(maxResults=10).execute()
    items = results.get('items', [])
    if not items:
        print('No files found.')
    else:
        print("Files:")
        for item in items:
            print(' {0} ({1})'.format(item['title'], item['id']))


print("""
Welcome to the setup of the uploader script. 
In this script you'll find a series of prompts and instructions to 
properly set up the settings.json and do it's best to simplify the
entire process.

Complete step 1 at https://developers.google.com/drive/v2/web/quickstart/python
which should assist you in obtaining your own client_secret.json 
that you will need for authentication. Copy it into the same directory
as this script.

Control+C to exit out of this script at any time, or press return to continue""")

if raw_input(">"):
    pass    

print("""
Copy and paste the following link into your browser to grant your project the ability
to use your google accounts' data. 

Generating URL to visit...""")
if raw_input(">"):
    pass

#printSettings()


try:
    authDriveTest()
except(InvalidClientSecretsError):
    print("""
Cannot locate client_secrets.json, 
please check to make sure the client_secrets.json file
is in the same directory as this script. Quitting.""")
    quit()
