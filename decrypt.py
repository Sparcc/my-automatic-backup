import hashlib
import getpass
import sys, os
import configparser
config = configparser.ConfigParser()
config.read('decrypt.ini')

def generatePassHash():
    temp = getpass.getpass().encode('utf-8')
    return hashlib.sha224(temp).hexdigest()

password = generatePassHash()
fileName = config['DEFAULT']['fileName']
# Not a typo: password is set: -p<password>
# https://sevenzip.osdn.jp/chm/cmdline/commands/extract_full.htm
os.system('7z x -p{p} {fn}.7z'.format(fn=fileName,p=password))
