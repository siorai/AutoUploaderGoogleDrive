import os
import fnmatch
import pprint
import logging
from AutoUploaderGoogleDrive.settings import categoriesDictSettings, torrentFileDirectory, googledrivedir, logfile



logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s %(message)s')

def Sort(directory=None, fullPath=None):
    """
    ....... yep. you guessed it. I'll explain this a bit more later as well....
    
    ....... soon though! <3 ........
    """
    global listOfFiles
    global torrentFileName
    listOfFiles = getListOfFiles(fullPath)
    logging.debug("SORT: Startup: listOfFiles: %s" % listOfFiles)
    torrentFileName = fetchTorrentFile(directory)
    logging.debug("SORT: Startup: torrentFileName: %s" % torrentFileName)
    setDict = categoriesDictSettings
    CategoriesDict = {
        'Music': {
            'Folder_ID': setDict
                ['Music']['Folder_ID'],
            'Rule': {
                'matchTracker': matchTracker('Music'),
                'matchExt': matchExt('Music')
            },
            'Matches': {
                'Match_Tracker': setDict
                    ['Music']['Matches']['Match_Tracker'],
                'Match_Content_Extention': setDict
                    ['Music']['Matches']['Match_Content_Extention']
            }
        },
        'TV':   {
            'Folder_ID': setDict
                ['TV']['Folder_ID'],
            'Rule': {
                'match_Tracker': matchTracker('TV'),
                'match_Pattern': matchPattern('TV')
            },
            'Matches': {
                'Match_Tracker': setDict
                    ['TV']['Matches']['Match_Tracker'],
                'Match_Expression': setDict
                    ['TV']['Matches']['Match_Expression']
                }
        },
        'Movies':   {
            'Folder_ID': setDict
                ['Movies']['Folder_ID'],
            'Rule' : {
                'Match_Tracker': matchTracker('Movies'),
                'Match_TV_Check': matchIsNotTV(),
                'Match_IsNotMusic': matchIsNotMusic()
            },
            'Matches': {
                'Match_Tracker': setDict
                    ['Movies']['Matches']['Match_Tracker']
            }
        },
        'XXX':  {
            'Folder_ID': setDict
                ['XXX']['Folder_ID'],
            'Rule' : {
                'matchTracker': matchTracker('XXX')
            },
            'Matches': {
                'Match_Tracker': setDict
                ['XXX']['Matches']['Match_Tracker']
            }
        }
    }
    for EachCategory in dict.fromkeys(CategoriesDict):
        logging.debug("SORT: Checking category: %s" % EachCategory)
        category = CategoriesDict[EachCategory]
        pprint.pprint(category)
        MatchesList = []
        for EachMatch in dict.fromkeys(category['Rule']):
            logging.debug("SORT: Checking %s" % EachMatch)
            EachRule = category['Rule'][EachMatch]
            MatchesList.append(EachRule)
            logging.debug("SORT: Added %s" % EachRule)
        logging.debug("SORT: MatchesList: %s" % MatchesList)
        MatchRequires = len(MatchesList)
        logging.debug("SORT: Requires Length: %s" % MatchRequires)
        MatchTrueCount = 0
        for EachMatch in MatchesList:
            if EachMatch is True:
                MatchTrueCount += 1
        if MatchTrueCount == MatchRequires:
            setFolder_ID = [
                EachCategory,
                category['Folder_ID']
            ]
            return setFolder_ID
    setFolder_ID = [
        "Default Directory",
        googledrivedir
        ]
    return setFolder_ID

def matchIsNotMusic():
    """
    Rule for ensuring there is no music file extentions
    in the files to help decrease possibility of a mis-sort.

    Args:
        None
    Returns:
        False if Match
        True if no Match
    """
    check = matchExt('Music')
    if check is True:
        return False
    else:
        return True

def matchTracker(category):
    """
    Rule for matching the tracker in the Torrent File by comparing
    the first line in the torrent and searching for each tracker 
    listed in the settings.

    Args:
        category: string. Category from CategoriesDict
    Returns:
        True if match
        False if no match
    """
    with open(torrentFileName, 'r') as TF:
        trackerInfo = TF.readline().split()[0]
    logging.debug("SORT: matchTracker: %s" % trackerInfo)
    trackerList = categoriesDictSettings[category]['Matches']['Match_Tracker']
    logging.debug("SORT: matchTracker: %s" % trackerList)
    for EachTracker in trackerList:
        logging.debug("SORT:matchTracker: %s" % EachTracker)
        if EachTracker in trackerInfo:
            return True
    return False

def fetchTorrentFile(directory):
    """
    Fetches the TorrentFile by matching the name to 'directory'
    
    Args:
        directory: string. Directory of files that the torrentfile 
            belongs to
    Return:
        filepath: string. /path/to/filename/of/Torrent.Torrent
    """
    fullFilePaths = directory
    folderName = fullFilePaths.rsplit(os.sep)
    logging.debug("SORT: fetchTorrentFile: Using %s" % folderName)
    bt_name = folderName[-1]
    logging.debug("SORT: fetchTorrentFile: %s" % bt_name)
    for path, dirs, files in os.walk(torrentFileDirectory):
        for EachTorrent in files:
            if bt_name in EachTorrent:
                filepath = os.path.join(path, EachTorrent)
                return filepath

def matchIsNotTV():
    """
    Rule for making sure the contents of the directory do not match
    the pattern for TV category.
    
    (Primarily used to ensure there are no Season Episode indicators
    in Movies)

    Args:
        None
    Returns:
        False if match
        True if no match
    """
    check = matchPattern('TV')
    if check is True:
        return False
    else:
        return True

def matchExt(category):
    """
    Rule for matching file extentions based on what's list in the settings, 
    for the category supplied.

    Args:
        category: string. Category from CategoriesDict
    Returns:
        True if match
        False if no match
    """
    categoryExtention = categoriesDictSettings[category]['Matches']['Match_Content_Extention']
    logging.debug("SORT: matchExt: %s" % categoryExtention)
    for EachExtention in categoryExtention:
        logging.debug("SORT: matchExt: trying %s" % EachExtention)
        for EachFile in listOfFiles:
            logging.debug("SORT: matchExt: trying %s inside of %s" % (EachExtention, EachFile))
            if fnmatch.fnmatch(EachFile, EachExtention):
                return True
    return False
       
def matchPattern(category):
    """
    Rule for matching a Pattern listed in the settings, for the category supplied

    Args:
        category: string. Category from CategoriesDict
    Returns:
        True if match
        False if no match
    """
    categoryPattern = categoriesDictSettings[category]['Matches']['Match_Expression']
    logging.debug("SORT: matchPattern: using %s" % categoryPattern)
    for EachPattern in categoryPattern:
        logging.debug("SORT: matchPattern: searching for %s" % EachPattern)
        for EachFile in listOfFiles:
            logging.debug("SORT: matchPattern: searching for %s in %s" % (EachPattern, EachFile))
            if fnmatch.fnmatchcase(EachFile, EachPattern):
                return True
    return False 

def getListOfFiles(directory):
    """
    Creates listOfFiles for iteration by various rules listed in Rules.py

    Args:
        directory: string. Directory to use to create the list of files
    Returns:
        listOfFiles: list. ....but really, it returns a 20 foot block of cheese.
    """
    listOfFiles = []
    for path, dirs, files in os.walk(directory):
        for eachFile in files:
            filePath = os.path.join(path, eachFile)
            listOfFiles.append(filePath)
    return listOfFiles
