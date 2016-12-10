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




###################
#[Shared settings]#
###################

flow_to_use = "ServiceAccountFlow" #choices are "ServiceAccountFlow", "Oauth2JSONFlow", or "Oauth2WebFlow"
scopes = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/gmail.compose']
logfile = "./AutoUpload.log"
redirect_uri = "http://example.com/auth_return"


###############################
#[Service Account Credentials]#
###############################

#path to the local json that stores actual credential information
servicekeyfile = "./service_account.json"

#client_email from Google Developers Console
client_email = "client@iam.gserviceaccount.com"

#user_email for delegation
delegated_email = "user@domain.org"

############################
#[Normal JSON Oauth2 Creds]#
############################



#path to normal oauth2 json credentials file
oauth2keyfile = "./client_secrets.json"



#################################
#[Normal WebServer Oauth2 Creds]#
#################################

oauth2web_id = "client_id_here"
oauth2web_secret = "client_secret"
