from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
import httplib2, logging, os
#import settings
import pickle
import json

from oauth2client import client

console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)


logging.getLogger('').addHandler(console)


#from AutoUploaderGoogleDrive.settingsjson import settingsLoader
from AutoUploaderGoogleDrive.settingsValidator import settingsLoader

"""
Class for creation of an authorized credential object

  Returns:
    Authorized credentials object for api call
"""

__author__ = 'siorai@gmail.com (Paul Waldorf)'

def makeJSON():
    """
    Initializes credentials flow by way of client.flow_from_clientsecrets
    and provies the user with a link to follow in a web-browser in order 
    to Authrize the Appication's ability to access the users files.

    Once it's authorized, the credentials object is then pickled into
    a file for later use. 
    """
    settings = settingsLoader()
    logging.basicConfig(filename=settings['logfile'],level=logging.DEBUG,format='%(asctime)s %(message)s')
    logging.debug("AUTH: JSON: flow_from_clientsecrets initialized")
    logging.debug("AUTH: JSON: Parameters used:")
    logging.debug("AUTH: JSON: oauth2keyfile: %s" % settings['oauth2KeyFile'])
    logging.debug("AUTH: JSON: Scopes=%s" % settings['scopes'])
    logging.debug("AUTH: JSON: redirect_uri=%s" % settings['redirectURI'])
    flow = client.flow_from_clientsecrets(
        settings['oauth2KeyFile'],
        scope=settings['scopes'],
        redirect_uri=settings['redirectURI'])
    flow.params['access_type'] = 'offline'
    auth_uri = flow.step1_get_authorize_url()
    print(auth_uri)
    logging.debug("AUTH: JSON: Auth_URL: %s" % auth_uri)
    auth_code = raw_input('Enter the authcode:')
    credentials = flow.step2_exchange(auth_code)
    http_auth = credentials.authorize(httplib2.Http())
    with open(settings['pickledCredsFile'], 'wb') as CF:
        pickle.dump(credentials, CF)
    logging.debug("AUTH: JSON: Created: %s" % settings['pickledCredsFile'])

def flowJSON():
    """
    Opens pickledcredsFile that contains all of the parameters
    needed to instantiate a Credentials object from the
    oauth2client.client

    """
    settings = settingsLoader()
    logging.basicConfig(filename=settings['logfile'],level=logging.DEBUG,format='%(asctime)s %(message)s')
    with open(settings['pickledCredsFile'], 'rb') as credentialsFile:
        credentials = pickle.load(credentialsFile)
    http_auth = credentials.authorize(httplib2.Http())
    logging.debug("AUTH: FLOW: Loaded Credentials from file")
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
    settings = settingsLoader()
    logging.basicConfig(filename=settings['logfile'],level=logging.DEBUG,format='%(asctime)s %(message)s')
    logging.debug("AUTH: Authoriziation initialized")
    flow = settings['flowToUse']
    if(flow == "ServiceAccountFlow"):
        logging.debug("AUTH: FLOW: Service Account Selected")
        http = serviceAccountCredential()
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
   
def serviceAccountCredential():
    """
    Utilizes the Service Account Credential flow to instantiate an authorized credentials
    object for calling the Google API
    """
    settings = settingsLoader()
    scopes = settings['scopes']
    settings = settings['serviceAccountCredentials']
    keyfile = settings['serviceKeyFile']
    logging.debug('AUTH: SAC_FLOW: Finished loading Service Account Keyfile: using %s' % keyfile )
    logging.debug('AUTH: SAC_FLOW: Loading scopes from settings file')
    logging.debug('AUTH: SAC_FLOW: Finished loading scopes from settings file')
    logging.debug('AUTH: SAC_FLOW: Initializing credential from oauth2client.service_account')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, 
                        scopes=scopes)
    logging.debug('AUTH: SAC_FLOW: Delegating credentials from settings')
    delegated_credentials = credentials.create_delegated(settings['delegatedEmail'])
    logging.debug('AUTH: SAC_FLOW:Initializing authorized, delegated credentials object')
    http = delegated_credentials.authorize(httplib2.Http())
    
    return http
