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
it functionality. Out of the box(... when it's completed of course).

For my own personal use, what I envision most others will also use it for, 
is to sit on a remote server, ie a seedbox, where torrents can be added 
remotely in any number of ways (remote-transmission for android, or the 
web-gui, etc). 

So what happens when you want to backup that hot new distro of slackware 
that just got released onto your Google Drive for safe keeping? 

Currently, there's a few tools around that will let you mount your 
Google Drive account straight to your filesystem. Most(all?) seem to default
around using the normal authentication flow written into the *apiclient* 
from Google. 

You can find details [here at on Google's Documentation Page](https://developers.google.com/identity/protocols/OAuth2) for specifics, but 
essentially it's a series of steps that have to be taken for any and all 
requests made to the Google API to use any of it's services. 

The problem, is that all of these requests require an additional level of account 
authorization that is granted based on either opening a page locally by calling a 
browser to open the 'Blahblah Application is requesting access to your Google Account.'
Where you supply your username and password to a browser window thus proving
to Google's servers that you, the owner of the account, is granting access to 
this program to your files or data contained in your account. 
This means it maintains a (imo at least) a reasonably high level of security 
to ensure the safety of your data. 

Here's an example of the normal auth flow: 

(Lets say we have a simple text editor that we'd like to load and save files from Google Drive.)

| El Grande Text Editor      | Request |           Das Google          |
|:--------------------------:|:-------:|:-----------------------------:|
|Hi Google! I'm Joe!         |  >>>>>  |                               |
|                            |  <<<<<  | Oh yeah? Prove it.            | (note1)
|Here's a code that proves it|  >>>>>  |                               | 
|                            |  <<<<<  | Cool, have a pair of tokens   |



(Note1: App is passed a webpage address that is then given to the user to 
visit and supply credentials, after which the user is given an authorization
code which is then entered into the app)

(Note2: The app repeats the same request)

At this point the Google Authentication Server issues out an access token,
and a refresh token if requested. The El Grande then uses this access token
to make authorized requests to the API. 

So what's the problem? They expire. What happens when they expire? You have
to request a new one, which means, you guessed it, going to that webpage,
supplying your credentials, and feeding that code back into El Grande.

But what about the refresh token? Could just use those right? Well, to put it 
mildly, refresh tokens are... *weird*. 

Here's what Google has to say about them: 


 
     "Note: Save refresh tokens in secure long-term storage and continue to
    use them as long as they remain valid. Limits apply to the number of
    refresh tokens that are issued per client-user combination, and per user
    across all clients, and these limits are different. If your application
    requests enough refresh tokens to go over one of the limits, older refresh
    tokens stop working."
   


There's no telling how long a refresh token will remain active. Plus, it means
that the application has to make calls to the API in regular intervals just to
keep the token alive, even if you aren't using it.

For AutoUploaderGoogleDrive, this means that unless I either make regular 
requests to the API, or otherwise constantly use it, the token granted
by that auth code becomes invalid. 

Numerous places in the oauth2 docs it talks about how developers should
develop their applications in anticipation of those tokens suddenly, randmoly, 
and mysteriously, just stop working. 

Now if I *had* to do that for the AutoUploaderGoogleDrive, well, I probably 
would, but thankfully, there's Service Accounts to address this very problem! 

How does using a Service Account fix this?
------------------------------------------

Creating and enabling a Service Account is currently a bit of a pain in the
ass. And if I had to guess, I'd assume that's by design. 

I'll go into the setup of those in a later point in time, but you essentially
go through a process that involves creating your own google project, and 
logging into the Google Developers console, going into some security settings
and creating the Service Account, and determining just what it can do (by 
enabling or disabling specific individual Google APIs).  

Right when you create it, it provides a link to a "projectnameblahblah.json" 
keyfile. This file is the **only one** that is generator for the Service 
Account. Forget to save it, or lose it, means you have to create a new Service
Account, therefor generating a new keyfile you hopefully won't lose. 

Once you have the keyfile, you use it in your app, (along with using an 
entirely different set of functions from the oauth2client library) the 
token exchange gets reduced. 

How reduced? Well from the end users point of view it essentially no longer
exists.  There's still a token exchange of course, but Google's Authentication 
Server gives up the token when it sees the Service Account Credential 
**without further interaction from either the application or the owner 
of the account**. 

Does the token you recieve from Google's Authentication Server ever expire?
Truthfully? I have no freaking idea. But what I -do- know, is  that it doesn't 
matter in the first place. Lose the token? Who cares. Get a new one with
the credentials. Token expire? Get a new one. Favorite tracker go down for
several weeks or even months and don't download any torrents for a while?
Fear not! That credential will remain valid until you, the owner/administrator
of that domain of Google Services pulls that credential from the developers
console by disableing  that account. 

Set it. And forget it. 

Got it? Good. Don't got it? I didn't either at first. Don't worry, you don't
need to know how it works, just how to set it up! 


 
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



Depends on Dependencies....
---------------------------


