from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
import httplib2, logging, os
import settings
import pickle
import json

from oauth2client import client

httplib2.debuglevel = settings.httplib2.debuglevel
settings.loggingSetup

"""
Class for creation of an authorized credential object

  Returns:
    Authorized credentials object for api call
"""


def makeJSON():
    """
    Initializes credentials flow by way of client.flow_from_clientsecrets
    and provies the user with a link to follow in a web-browser in order 
    to Authrize the Appication's ability to access the users files.

    Once it's authorized, the credentials object is then pickled into
    a file for later use. 
    """
    logging.debug("AUTH: JSON: flow_from_clientsecrets initialized")
    logging.debug("AUTH: JSON: Parameters used:")
    logging.debug("AUTH: JSON: oauth2keyfile: %s" % settings.oauth2keyfile)
    logging.debug("AUTH: JSON: Scopes=%s" % settings.scopes)
    logging.debug("AUTH: JSON: redirect_uri=%s" % settings.redirect_uri)
    flow = client.flow_from_clientsecrets(
        settings.oauth2keyfile,
        scope=settings.scopes,
        redirect_uri=settings.redirect_uri)
    flow.params['access_type'] = 'offline'
    auth_uri = flow.step1_get_authorize_url()
    print(auth_uri)
    logging.debug("AUTH: JSON: Auth_URL: %s" % auth_uri)
    auth_code = raw_input('Enter the authcode:')
    credentials = flow.step2_exchange(auth_code)
    http_auth = credentials.authorize(httplib2.Http())
    with open(settings.pickledcredsFile, 'wb') as CF:
        pickle.dump(credentials, CF)
    logging.debug("AUTH: JSON: Created: %s" % settings.pickledcredsFile)

def flowJSON():
    """
    Opens pickledcredsFile that contains all of the parameters
    needed to instantiate a Credentials object from the
    oauth2client.client

    """
    with open(settings.pickledcredsFile, 'rb') as CF:
        credentials = pickle.load(CF)
    http_auth = credentials.authorize(httplib2.Http())
    logging.debug("AUTH: FLOW: Loaded Credentials from file")
    logging.debug("AUTH: FLOW: %s" % credentials)
    return http_auth

def Authorize():
    """
    Fetches correct flow_to_use and builds accordingly.
    
    Currently only ServiceAccountFlow and Oauth2JSONFlow
    are implimented. 

    In the case of Oauth2JSONFlow, flowJSON attempts to
    open the pickledcredsFile, if it fails, it creates one
    with makeJSON(), saves it, and then attempts to
    open it by re-executing flowJSON.    
    """
    logging.debug("AUTH: Authoriziation initialized")
    flow = settings.flow_to_use
    if(flow == "ServiceAccountFlow"):
        logging.debug("AUTH: FLOW: Service Account Selected")
        http = Service_Account_Credential()
        logging.debug("AUTH: SAC_FLOW: Service Account loaded")
        return http
    if(flow == "Oauth2JSONFlow"):
        logging.debug("AUTH: FLOW: JSONFlow Selected")
        try:
            http = flowJSON()
            return http
        except:
            makeJSON()
        try:   
            http = flowJSON()
            return http
        except:
            print("Still not working, sorry")
            quit()
    else:
        logging.debug("AUTH: Nothing found!")
   
def Service_Account_Credential():
    """
    Utilizes the Service Account Credential flow to instantiate an authorized credentials
    object for calling the Google API
    """
    logging.debug('DEBUG: SAC_FLOW: Attemping to load settings file from %s' % settings.servicekeyfile)
    keyfile = settings.servicekeyfile
    logging.debug('DEBUG: SAC_FLOW: Finished loading Service Account Keyfile: using %s' % keyfile )
    logging.debug('DEBUG: SAC_FLOW: Loading scopes from settings file')
    scopes = settings.scopes
    logging.debug('DEBUG: SAC_FLOW: Finished loading scopes from settings file')
    logging.debug('DEBUG: SAC_FLOW: Initializing credential from oauth2client.service_account')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, 
                        scopes=scopes)
    logging.debug('DEBUG: SAC_FLOW: Delegating credentials from settings')
    delegated_credentials = credentials.create_delegated(settings.delegated_email)
    logging.debug('DEBUG: SAC_FLOW:Initializing authorized, delegated credentials object')
    http = delegated_credentials.authorize(httplib2.Http())
    
    return http
