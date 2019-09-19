from BackupUtils import *
import sys
import os
sys.path.append(os.getcwd())


cwd = os.getcwd()
sys.path.append(cwd)
config = configparser.ConfigParser()
config.read('backup.ini')
backupSources = config['DEFAULT']['backupSources'].split(",")
backupdDestinations = config['DEFAULT']['backupDestinations'].split(",")
standardCopyOptions = config['DEFAULT']['standardCopyOptions']
passwordExists = config['DEFAULT']['encryptionKey']
passwordExists = passwordExists.lower()

# Check if we are using encryption then we should ask for password
encryptedBackupEnabled = False
for destination in backupdDestinations:
    if re.search('.*encrypted.*', destination):
        encryptedBackupEnabled = True
        break
password = ''
if encryptedBackupEnabled:
    password = createPassword(passwordExists, config)
    
ignoreNames = config['DEFAULT']['ignore']
for source in backupSources:
    source = source.strip()
    print('processing source ' + source)
    for destination in backupdDestinations:
        print('processing destination ' + destination)
        destination = destination.strip()
        logging = backupSourceToDestination(
            source, destination, password, standardCopyOptions)
        print(logging)