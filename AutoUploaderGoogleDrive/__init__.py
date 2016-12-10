from AutoUploaderGoogleDrive.emailtest import main, encode_message, send_message, get_filepaths
from AutoUploaderGoogleDrive.upload import upload
from AutoUploaderGoogleDrive.temp import setup_temp_file, addentry, finish_html
from AutoUploaderGoogleDrive.settings import logfile

import logging


__version__ = '0.0.1'
__author__ = 'Paul Waldorf'

logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info('AutoUploaderGoogleDrive initilized.')

