""" Libray for creating a temporary html file to be encoded by
emailtest.py that contains a table listing all the files uploaded, 
the time the torrent was finished, and a link to that file
"""

__author__ = 'siorai@gmail.com (Paul Waldorf)'

import os
import tempfile
import logging

from AutoUploaderGoogleDrive.settings import logfile
import upload

#Module for the creation and population of a temporary W3C Validated HTML file
#containing an a table to be compiled using AutoUploaderGoogleDrive.upload.encode_message 


logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s %(message)s')

tempfilename = '/var/tmp/transmissiontemp/transmission.%s.html' % os.getpid()

def setup_temp_file(tempfilename):
  """ 
  Creates an html file with initial tags 
  to be ultimately encoded in the encode_message
  function. Sets up the initial table with 'Time
  Uploaded', 'File size in bytes', 'File Name',
  and 'Link to File'. Where link is direct link supplied
  from Google Drive.

  Args:
   
    tempfilename: path/to/temp/file/name
    
  Returns:
    
    Nothing
  
  """
  print 'Building a tempfile:'
  logging.debug('TEMP: Creating html file %s' % tempfilename)
  htmlfile = open(tempfilename, 'w')
  logging.debug('TEMP: %s created.' % tempfilename)

  message = """<!DOCTYPE HTML SYSTEM>
<html>
<head><title></title></head>
<body><p>
<table style="width:100%">
  <tr>
    <th>Time Uploaded</th>
    <th>File size in bytes</th>
    <th>File Name</th>
    <th>Link to File</th>
  </tr>"""

  htmlfile.write(message)
  htmlfile.close()
  logging.debug('%s created.' % tempfilename)



def addentry(tempfilename, time_uploaded, file_size_bytes, name_of_file, direct_gdrive_link):
  """ 
  Appends the temp html file by adding a row 
  in the table for each entry in the list supplied from 
  AutoUploaderGoogleDrive.emailtest.get_filepaths
  
  Args:
    tempfilename: path/to/temp/file/name
    time_uploaded: string returned from os.getenv('TR_TIME_LOCALTIME') 
    file_size_bytes: int returned from os.path.getsize
    name_of_file: string returned from list returned by
    AutoUploaderGoogleDrive.emailtest.get_filepaths
    direct_gdrive_link: direct link to file's location on Google Drive
  
  
  """  
  logging.debug('Opening %s to add entry %s' % (tempfilename, name_of_file)) 
  append = open(tempfilename, 'a')
  
  table_entry = """  
  <tr>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
  </tr>""" % (time_uploaded, file_size_bytes, name_of_file, direct_gdrive_link)             

  append.write (table_entry)
  append.close()
  logging.debug('Added %s entry to %s' % (name_of_file, tempfilename ))

def finish_html(tempfilename):
  """ 
  Closes up the html temp file and closes the tags
  
  Args: 
    tempfilename: path/to/temp/file/name
    
  Returns:
    Nothing
  """	

  append = open(tempfilename, 'a')
  finish_up = """
</table>
</body>
</html>"""
  
  append.write(finish_up)
  append.close()
  logging.debug('Wrapping up html in %s' % tempfilename )



