# AutoUploaderGoogleDrive
AutoUploaderGoogleDrive
=======================

What's it all about?
--------------------

*AutoUploaderGoogleDrive* is a module currently in progress that will process
finished files after torrent completion and send them to a specific Google 
Drive account.

Alright then, so what'cha done so far?
-------------------

Glad you asked! 

- *setup.py*
  Setuptools script to add 'AutoUploaderGoogleDrive' to console commands
  in order for the transmission-daemon to call it directly
- *README.md*
  Some fairly outdated file that chances are has no real information and won't 
  be of any use to anyone at any given point in time.
  
  

- *AutoUploaderGoogleDRive/if_you_error_on_this_file_it_worked.json* 
  Placeholder for JSON keyfile to be replaced by one supplied from google when
  ServiceLevelAuthentication is activated
- *AutoUploaderGoogleDrive/emailtest.py*
  Current main portion of the script, when supplied with correct credentials 
  settings.py it'll either email a list containing all of the files that were
  just downloaded from the torrent (if executed from the transmission-daemon)
  otherwise just defaults to the PWD
- *AutoUploaderGoogleDrive/temp.py*
  Library for creating a temporary, W3C HTML 4.01 strict compliant file that 
  contains a table that will populate with data when executed from 
  AutoUploaderGoogleDriver.emailtest (Functional, but not implimented into 
  emailtest just quite yet)
- *AutoUploaderGoogleDrive/upload.py*
  Library that handles the ServiceAccount object creation for uploading of
  files to Google Drive. Newest implimentation of the upload function remains 
  untested, however it was verified as working when executed alone via 

::

    $ python upload.py /path/to/file.name
    
::

  and would print a link in the console to it's location on Google Drive




