import sys, os
import configparser
import re
import hashlib
import getpass
def generatePassHash():
    temp = getpass.getpass().encode('utf-8')
    return hashlib.sha224(temp).hexdigest()
password=generatePassHash()
cwd = os.getcwd()
sys.path.append(cwd)
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
        folderName=re.search('.*(\\\.+)',source).groups()[0][1:-1]
        if re.search('.*encrypted.*',destination):
            try:
                print('FOLDER NAME IS '+folderName)
                print('\nCREATING ARCHIVE')
                os.system('7za a -mhe=on -p{p} {fn}.7z {d}'.format(fn=folderName,p=password,d=source))
                print('\nCREATING DIRECTORY')
                os.system('mkdir {d}\{fn}"'.format(fn=folderName,d=destination[:-1]))
                print('\nCOPYING ARCHIVE TO NEW DIRECTORY')
                os.system('copy {fn}.7z {d}\{fn}"'.format(fn=folderName,d=destination[:-1]))
                print('\nREMOVING SOURCE ARCHIVE')
                os.system('del {fn}.7z'.format(fn=folderName))
                successMessage+='>"{s}" has been successfully backed up securely to {b}\n'.format(s=folderName,b=destination)
            except:
                successMessage+='>"{s}" back up to {b} has failed\n'.format(s=folderName,b=destination)
                pass
        else:
            try:
                os.system('robocopy {bs} {rco} {bl}\{fn}"'.format(bs=source,rco=roboCopyOptions,bl=destination[:-1],fn=folderName))
                successMessage+='>"{s}" has been successfully backed up to {b}\n'.format(s=folderName,b=destination)
            except:
                successMessage+='>"{s}" back up to {b} has failed\n'.format(s=folderName,b=destination)
                pass
print(successMessage)
