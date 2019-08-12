import re,os

class BackupTools:
    def __init__(self, options=None):
        self.options = options

    def: canBackup(self, fileName):
        select
        if (self.options)

    def getFolderName(self, source):
        endOfPath = r'^\".:\\?.*?.*\\(.*)\"$'
        print('source='+source)
        folderName=re.search(endOfPath,source).groups()[0]
        return folderName
        

    def doEncryptedBackup(self, source, destination, password, options=None):
        logging = ''
        print('source='+source)
        folderName=self.getFolderName(source)
        print('folderName='+folderName)
        try:
            print('\nCREATING ARCHIVE FOR {fn}'.format(fn=folderName))
            os.system('7z a "{fn}.7z" {d} -p{p} -mhe'.format(p=password,fn=folderName,d=source))

            print('\n----CREATING DIRECTORY')
            os.system('mkdir {d}\{fn}"'.format(fn=folderName,d=destination[:-1]))

            print('\n----COPYING ARCHIVE FROM SOURCE TO DESTINATION\FILENAME')
            os.system('copy "{fn}.7z" "{d}\{fn}"'.format(fn=folderName,d=destination[1:-1]))
            os.system('copy decrypt.py "{d}\{fn}"'.format(d=destination[1:-1],fn=folderName))
            os.system('copy decrypt.ini "{d}\{fn}"'.format(d=destination[1:-1],fn=folderName))
            os.system('copy decrypt.bat "{d}\{fn}"'.format(d=destination[1:-1],fn=folderName))

            print('\n----REMOVING SOURCE ARCHIVE')
            os.system('del "{fn}.7z"'.format(fn=folderName))
            logging+='>"{s}" has been successfully backed up securely to {b}\n'.format(s=folderName,b=destination)

        except:
            logging+='>"{s}" back up to {b} has failed\n'.format(s=folderName,b=destination)
            pass

        return logging

    def doStandardBackup(self, source, destination, options=None):
        logging = ''
        folderName=self.getFolderName(source)
        try:
            print('\n----COPYING SOURCE TO DESTINATION\FILENAME')
            os.system('robocopy {bs} {rco} "{bl}\{fn}"'.format(bs=source,rco=options[1:-1],bl=destination[1:-1],fn=folderName))
            logging+='>"{s}" has been successfully backed up to {b}\n'.format(s=folderName,b=destination)

        except:
            logging+='>"{s}" back up to {b} has failed\n'.format(s=folderName,b=destination)
            pass

        return logging
