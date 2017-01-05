from __future__ import print_function
import ConfigParser, os 
from sys import argv

from apiclient import discovery
import auth
import settings
from auth import Authorize

from apiclient import discovery
from apiclient.http import MediaFileUpload

#Command arguments to test functionality, should be passed via torrent in future
script, filename = argv

http = Authorize()

serviceDrive = discovery.build('drive', 'v2', http=http)



#Function for uploading filename set in argv when executed
def main(filename):
    FilePath = os.path.abspath(filename)
    body = {
            'title': filename
    }
    body['parents'] = [{'id' : settings.googledrivedir}]
    media = MediaFileUpload(FilePath, chunksize=settings.chunksize, resumable=True)
    response = serviceDrive.files().insert(body=body, media_body=media).execute()
    if settings.nonDefaultPermissions == True:
        fileID = response['id']
        setPermissions(fileID)
    print(response['alternateLink'])
     
def setPermissions(file_id):
    service = serviceDrive
    newPermissions = {
        'value': settings.permissionValue,
        'type': settings.permissionType,
        'role': settings.permissionRole
    }
    return service.permissions().insert(fileId=file_id,
        body=newPermissions).execute()

if __name__ == '__main__':
    main(filename)
