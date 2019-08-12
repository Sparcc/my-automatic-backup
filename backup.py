import sys,os
sys.path.append(os.getcwd())
from BackupUtils import *


cwd = os.getcwd()
sys.path.append(cwd)
config = configparser.ConfigParser()
config.read('backup.ini')
backupSources = config['DEFAULT']['backupSources'].split(",")
backupdDestinations = config['DEFAULT']['backupDestinations'].split(",")
standardCopyOptions = config['DEFAULT']['standardCopyOptions']
passwordExists = config['DEFAULT']['encryptionKey']
passwordExists = passwordExists.lower()
password = createPassword(passwordExists, config)
ignoreNames = 

for source in backupSources:
    source = source.strip()

    for destination in backupdDestinations:
        destination = destination.strip()
        logging = backupSourceToDestination(source, destination, password, standardCopyOptions)
        print(logging)
