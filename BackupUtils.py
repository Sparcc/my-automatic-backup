import sys
import os
import configparser
import re
import hashlib
import getpass
from BackupTools import *
backupTools = BackupTools()

def _canSkip(folderName, folderIgnorePatterns):
    print('*********starting logging _canSkip************')
    print(folderName)
    print(folderIgnorePatterns)
    print('*********finished logging _canSkip************')

    #'''
    for ignorePat in folderIgnorePatterns:
        
        sr = re.search(ignorePat, folderName)
        # Ensure full match of pattern
        if (sr and len(sr[0]) == len(folderName)):
            print(folderName+' VS '+ignorePat+'=pass')
            print('group match='+sr[0])
            print('ignoring '+folderName)
            return True

    #'''
    return False

def _generatePassHash():
    temp = getpass.getpass().encode('utf-8')
    return hashlib.sha224(temp).hexdigest()


'''
_createPassword

parameters:
passwordExists - Can be: not_set, none, null, set
config - configParser object reference not copy
'''


def createPassword(passwordExists, config):

    password = ''

    cwd = os.getcwd()
    files = os.listdir(cwd)
    if ('key' not in files):
        print("ERROR - 'key' file does not exist")
        open('key', 'w+')

    if (
            passwordExists == 'not_set' or
            passwordExists == 'none' or
            passwordExists == 'null' or
            passwordExists == 'false'):  # Initial case
        password = _generatePassHash()
        print('STORING PASSWORD')
        config['DEFAULT']['encryptionKey'] = 'SET'
        f = open('key', 'w')
        f.write(password)
        with open('backup.ini', 'w') as configfile:
            config.write(configfile)
    elif passwordExists.lower() == 'set':  # Case where password was set before
        f = open('key', 'r')
        password = f.read()

    return password


'''
_backupSourceToDestination

parameters:
source - Source folder path
destination - destination folder path
password - used to encrypt
'''


def backupSourceToDestination(
    source, 
    destination, 
    password=None, 
    standardCopyOptions=None, 
    encryptedCopyOptions=None, 
    folderIgnorePatterns=None
    ):
    # Build folder name automaticalyl with source name if no folder exists in destination for use later on
    logging = ''
    # Encryption backup
    folderName = backupTools.getFolderName(source)
    if (re.search('.*encrypted.*', destination) and password is not None):  # IF encryption is needed
        # extract drive letter of destination
        match = re.search('([A-Z]:)', destination)
        # IF extraction successful AND IF the drive letter exists then build archive
        if match and os.path.exists(match.groups()[0]):
            configDecrypt = configparser.ConfigParser()
            configDecrypt.read('decrypt.ini')

            print(folderIgnorePatterns)
            if folderIgnorePatterns:
                if _canSkip(folderName, folderIgnorePatterns):
                    return ('Ignoring' +source+ ' to ' +destination)
                
            fileName = folderName
            configDecrypt['DEFAULT']['fileName'] = '"'+fileName+'"'
            with open('decrypt.ini', 'w') as configfile:
                configDecrypt.write(configfile)
            logging = backupTools.doEncryptedBackup(
                source, destination, password)
    # Standard backup
    else:
        #print('ignorePatterns='+ignorePatterns)
        #'''
        if folderIgnorePatterns:
            if _canSkip(folderName, folderIgnorePatterns):
                
                return 'skipping'
                #return ('Ignoring' +source+ ' to ' +destination)
        #'''
        logging = backupTools.doStandardBackup(
            source, destination, standardCopyOptions)

    return logging
