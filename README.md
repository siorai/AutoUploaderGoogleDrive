AutoUploaderGoogleDrive
=======================

What's it all about?
--------------------

*AutoUploaderGoogleDrive* is a module currently in progress that will process
finished files after torrent completion and send them to a specific Google 
Drive account.


How's it work? (Or will when it's finished?)
--------------------------------------------

This script talks to the Google API and uploads the files it gets passed
by the transmission-daemon. The script utilizes it's own oauth2 
authentication flow based on the oauth2client.service_account library. 

*AutoUploaderGoogleDrive* is unique in that it was designed from the ground
up in order to access the Google API through a Service Level Account. Although
I'll still add a normal authentication flow for folks that would rather use 
the normal way of authentication. 

Is accessing the google api via ServiceAccount authentication *really* needed?
Probably not. But it has one seriously strong advantage in this partucular 
usage case. 

Complete elimination of user interaction whatsoever. Genuine set it and forget
it functionality. Out of the box(... when it's completely of course).



Alright then, so what'cha done so far?
--------------------------------------

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



Depends on Dependancies....
---------------------------


