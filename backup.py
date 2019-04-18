import sys,os
sys.path.append(os.getcwd())
from BackupUtils import *


cwd = os.getcwd()
sys.path.append(cwd)
config = configparser.ConfigParser()
config.read('backup.ini')
backupSources = config['DEFAULT']['backupSources'].split(",")
backupdDestinations = config['DEFAULT']['backupDestinations'].split(",")
roboCopyOptions = config['DEFAULT']['roboCopyOptions'][1:-1]
passwordExists = config['DEFAULT']['encryptionKey']
passwordExists = passwordExists.lower()
password = createPassword(passwordExists, config)

for source in backupSources:
    source = source.strip()

    for destination in backupdDestinations:
        destination = destination.strip()
        logging = backupSourceToDestination(source, destination, password, roboCopyOptions)
        print(logging)
