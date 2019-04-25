import sys,os
import configparser
import re
import hashlib
import getpass
from BackupTools import *
backupTools = BackupTools()

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

    if passwordExists == 'not_set' or passwordExists == 'none' or passwordExists == 'null': # Initial case
        password = _generatePassHash()
        print('STORING PASSWORD')
        config['DEFAULT']['encryptionKey'] = 'SET'
        f = open('key','w')
        f.write(password)
        with open('backup.ini', 'w') as configfile:
            config.write(configfile)
    elif passwordExists.lower() == 'set': # Case where password was set before
        f = open('key','r')
        password = f.read()

    return password

'''
_backupSourceToDestination

parameters:
source - Source folder path
destination - destination folder path
password - used to encrypt
'''
def backupSourceToDestination(source, destination, password=None, standardCopyOptions=None, encryptedCopyOptions=None):
    # Build folder name automaticalyl with source name if no folder exists in destination for use later on
    logging = ''
    # Encryption backup
    
    if re.search('.*encrypted.*',destination): # IF encryption is needed
        match = re.search('([A-Z]:)',destination) #extract drive letter of destination
        if match and os.path.exists(match.groups()[0]): #IF extraction successful AND IF the drive letter exists then build archive
            configDecrypt = configparser.ConfigParser()
            configDecrypt.read('decrypt.ini')
            fileName=backupTools.getFolderName(source)
            configDecrypt['DEFAULT']['fileName'] = '"'+fileName+'"'
            with open('decrypt.ini', 'w') as configfile:
                configDecrypt.write(configfile)
            logging = backupTools.doEncryptedBackup(source, destination, password)
    # Standard backup
    else:
        logging = backupTools.doStandardBackup(source, destination, standardCopyOptions)
    
    return logging
