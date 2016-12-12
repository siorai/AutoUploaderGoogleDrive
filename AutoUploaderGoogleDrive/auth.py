from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
import httplib2, logging, os
import settings

httplib2.debuglevel = 4

logging.basicConfig(filename=settings.logfile,level=logging.DEBUG,format='%(asctime)s %(message)s')

"""
Class for creation of an authorized credential object

  Returns:
    Authorized credentials object for api call
"""
    

def Authorize():
	
    """
    Fetches correct flow_to_use and builds accordingly
    """

    logging.debug('DEBUG: Authorization initialized')
    flow = settings.flow_to_use

    if(flow == "ServiceAccountFlow"):
      logging.debug("DEBUG: FLOW: Service Account Selected!")
      http = Service_Account_Credential()
      return http
    elif(flow == "Oauth2JSONFlow"):
      print("Oauth2JSON selected!")
    elif(flow == "Oauth2WebFlow"):
      print("Oauth2WebFlow selected!")
    else:
      print("Nothing found!")
   
def Service_Account_Credential():
	
    logging.debug('DEBUG: SAC_FLOW: Attemping to load settings file from %s' % settings.servicekeyfile)
    keyfile = settings.servicekeyfile
    logging.debug('DEBUG: SAC_FLOW: Finished loading Service Account Keyfile: using %s' % keyfile )
    logging.debug('DEBUG: SAC_FLOW: Loading scopes from settings file')
    scopes = settings.scopes
    logging.debug('DEBUG: SAC_FLOW: Finished loading scopes from settings file')
    logging.debug('DEBUG: SAC_FLOW: Initializing credential from oauth2client.service_account')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, 
                        scopes=scopes)
    logging.debug('Delegating credentials from settings')
    delegated_credentials = credentials.create_delegated(settings.delegated_email)
    logging.debug('Initializing authorized, delegated credentials object')
    http = delegated_credentials.authorize(httplib2.Http())
    
    return http
