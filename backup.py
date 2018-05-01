import sys, os
import configparser
import re
sys.path.append(os.getcwd())
config = configparser.ConfigParser()
config.read('backup.ini')
backupSources = config['DEFAULT']['backupSources'].split(",")
backupdDestinations = config['DEFAULT']['backupDestinations'].split(",")
roboCopyOptions = config['DEFAULT']['roboCopyOptions'][1:-1]
successMessage=''
for source in backupSources:
    source = source.strip()
    for destination in backupdDestinations:
        destination = destination.strip()
        folderName=re.search('.*(\\\.+)',source).groups()[0]
        try:
            os.system('robocopy {bs} {rco} {bl}{fn}'.format(bs=source,rco=roboCopyOptions,bl=destination,fn=folderName))
            successMessage+='>"{s}" has been successfully backed up to {b}\n'.format(s=folderName[1:-1],b=destination)
        except:
            successMessage+='>"{s}" back up to {b} has failed\n'.format(s=folderName[1:-1],b=destination)
            pass
print(successMessage)
