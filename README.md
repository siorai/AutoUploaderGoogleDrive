# AutoUploaderGoogleDrive
Uploading Script to send completed torrents to Google Drive automatically

Goal: 

To create a script that will automatically run at the time of torrent completion to upload to Google Drive.

Completed so far: 

Command line script that uploads a file (as determined by an argument passed when run) to google drive. 

Features to be implemented: 

- Send email notifying user of upload completion, with stats such as speed, size, and folder, along with including a link to the relative files and/or folders 

- Detect archives in completed files and, if found, extract those contents, upload them to Google Drive, and then delete extracted contents leaving original archives intact for the purposes of seeding

- Detect and recognize individual files/extracted contents and upload them to the folders they should go, (possibly with just the file extension)

