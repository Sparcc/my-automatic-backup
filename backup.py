import sys, os
import configparser
import re
import hashlib
import getpass
def generatePassHash():
    temp = getpass.getpass().encode('utf-8')
    return hashlib.sha224(temp).hexdigest()
cwd = os.getcwd()
sys.path.append(cwd)
config = configparser.ConfigParser()
config.read('backup.ini')
backupSources = config['DEFAULT']['backupSources'].split(",")
backupdDestinations = config['DEFAULT']['backupDestinations'].split(",")
roboCopyOptions = config['DEFAULT']['roboCopyOptions'][1:-1]
passwordExists = config['DEFAULT']['encryptionKey']
passwordExists = passwordExists.lower()
password = 'password'
if passwordExists == 'not_set' or passwordExists == 'none' or passwordExists == 'null':
    password=generatePassHash()
    print('STORING PASSWORD')
    config['DEFAULT']['encryptionKey'] = 'SET'
    f = open('key','w')
    f.write(password)
    with open('backup.ini', 'w') as configfile:
        config.write(configfile)
elif passwordExists.lower() == 'set':
    f = open('key','r')
    password = f.read()
successMessage=''
for source in backupSources:
    source = source.strip()
    for destination in backupdDestinations:
        destination = destination.strip()
        folderName=re.search('.*(\\\.+)',source).groups()[0][1:-1]
        unencryptedBackup = True
        if re.search('.*encrypted.*',destination): #if encryption is needed
            match = re.search('([A-Z]:)',destination) #extract drive letter of destination
            if match: #if extraction successful
                if os.path.exists(match.groups()[0]): #if the drive letter exists then build archive
                    unencryptedBackup = False #dont do the other unencrypted backup type
                    configDecrypt = configparser.ConfigParser()
                    configDecrypt.read('decrypt.ini')
                    configDecrypt['DEFAULT']['fileName'] = '"'+folderName+'"'
                    with open('decrypt.ini', 'w') as configfile:
                        configDecrypt.write(configfile)
                    try:
                        print('FOLDER NAME IS '+folderName)
                        print('\nCREATING ARCHIVE')
                        os.system('7za a -mhe=on -p{p} {fn}.7z {d}'.format(fn=folderName,p=password,d=source))
                        print('\nCREATING DIRECTORY')
                        os.system('mkdir {d}\{fn}"'.format(fn=folderName,d=destination[:-1]))
                        print('\nCOPYING ARCHIVE TO NEW DIRECTORY')
                        os.system('copy {fn}.7z {d}\{fn}"'.format(fn=folderName,d=destination[:-1]))
                        os.system('copy decrypt.py {d}\{fn}"'.format(fn=folderName,d=destination[:-1]))
                        os.system('copy decrypt.ini {d}\{fn}"'.format(fn=folderName,d=destination[:-1]))
                        print('\nREMOVING SOURCE ARCHIVE')
                        os.system('del {fn}.7z'.format(fn=folderName))
                        successMessage+='>"{s}" has been successfully backed up securely to {b}\n'.format(s=folderName,b=destination)
                    except:
                        successMessage+='>"{s}" back up to {b} has failed\n'.format(s=folderName,b=destination)
                        pass
        if unencryptedBackup:
            try:
                os.system('robocopy {bs} {rco} {bl}\{fn}"'.format(bs=source,rco=roboCopyOptions,bl=destination[:-1],fn=folderName))
                successMessage+='>"{s}" has been successfully backed up to {b}\n'.format(s=folderName,b=destination)
            except:
                successMessage+='>"{s}" back up to {b} has failed\n'.format(s=folderName,b=destination)
                pass
print(successMessage)
