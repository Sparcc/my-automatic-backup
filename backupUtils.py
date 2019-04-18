import sys,os
sys.path.append(os.getcwd())
import configparser
import re
import hashlib
import getpass

'''
_createPassword

parameters:
passwordExists - Can be: not_set, none, null, set
config - configParser object reference not copy
'''
def _createPassword(passwordExists, config):
        password = ''

        if passwordExists == 'not_set' or passwordExists == 'none' or passwordExists == 'null': # Initial case
        password=_generatePassHash()
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
def _backupSourceToDestination(source, destination, password):
    # Build folder name automaticalyl with source name if no folder exists in destination for use later on
    folderName=re.search('.*(\\\.+)',source).groups()[0][1:-1]
    logging = ''
    # Encryption backup
        if re.search('.*encrypted.*',destination): # IF encryption is needed
            match = re.search('([A-Z]:)',destination) #extract drive letter of destination
            if match: # IF extraction successful
                if os.path.exists(match.groups()[0]): #IF the drive letter exists then build archive
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
                        logging+='>"{s}" has been successfully backed up securely to {b}\n'.format(s=folderName,b=destination)
                    except:
                        logging+='>"{s}" back up to {b} has failed\n'.format(s=folderName,b=destination)
                        pass
        # Standard backup
        else:
            try:
                os.system('robocopy {bs} {rco} {bl}\{fn}"'.format(bs=source,rco=roboCopyOptions,bl=destination[:-1],fn=folderName))
                logging+='>"{s}" has been successfully backed up to {b}\n'.format(s=folderName,b=destination)
            except:
                logging+='>"{s}" back up to {b} has failed\n'.format(s=folderName,b=destination)
                pass
        
        return logging