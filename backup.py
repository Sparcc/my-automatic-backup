import backupUtils

def _generatePassHash():
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
password = _createPassword(passwordExists, config)

for source in backupSources:
    source = source.strip()

    for destination in backupdDestinations:
        destination = destination.strip()
        logging += _backupSourceToDestination(source,destination,password)
        print(logging)
