""" Libray for creating a temporary html file to be encoded by
emailtest.py that contains a table listing all the files uploaded, 
the time the torrent was finished, and a link to that file
"""

__author__ = 'siorai@gmail.com (Paul Waldorf)'

import os
import tempfile
import logging

from AutoUploaderGoogleDrive.settings import logfile, emailparameters
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
    logging.debug('TEMP: Creating html file %s' % tempfilename)
    htmlfile = open(tempfilename, 'w')
    logging.debug('TEMP: %s created.' % tempfilename)
    message = """<!DOCTYPE HTML SYSTEM>
<html>
<head><title></title></head>
<body><p>
<table style="width:100%">
  <tr>"""
    htmlfile.write(message)
    htmlfile.close
    htmlfile = open(tempfilename, 'a')
    for EachHeader in emailparameters:
        TableHeader = """
    <th>%s</th>""" % (EachHeader)
        htmlfile.write(TableHeader)
    htmlfile.write("""
  </tr>""")
    htmlfile.close
    logging.debug('%s created.' % tempfilename)
    


def addentry(tempfilename, JData):
    """ 
    Appends the temp html file by adding a row 
    in the table for each entry in the list supplied from 
    AutoUploaderGoogleDrive.emailtest.get_filepaths
  
    Args:
        tempfilename: path/to/temp/file/name
        JData: JSON data to be parsed to pull information from
    
  
  
    """  
    #logging.debug('TABLE: Opening %s to append entry') % tempfilename
    append = open(tempfilename, 'a')
    RowTag = """
  <tr>"""
    append.write(RowTag)
    for EachEntry in emailparameters:          
        Entry = """
    <td>%s</td>""" % JData[EachEntry]
        append.write(Entry)
    RowEnd = """
  </tr>"""
    append.close()
    #logging.debug('TABLE: Added %s entry to %s') % (name_of_file, name_of_file)

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
  #logging.debug('Wrapping up html in %s' % tempfilename )



