import sys, os
import configparser
def str2bool(v):
    returnValue = False
    if v.lower() in ("yes", "true", "t"):
        returnValue = True
    elif v.lower() in ("no", "false", "f"):
        returnValue = False
    return returnValue
config = configparser.ConfigParser()
config.read('deploy.ini')
items = config['DEFAULT']['items'].split(",")
locations = config['DEFAULT']['locations'].split(",")
ignoreConfiguration = str2bool(config['DEFAULT']['ignoreConfiguration'])
for item in items:
    item = item.strip()[1:-1]
    print('LOOKING AT ITEM '+item)
    if ignoreConfiguration and item[len(item)-3:] == "ini" and item != 'decrypt.ini':
        print('Skipping configuration file: '+item)
    else:
        for location in locations:
            location = location.strip()
            os.system('mkdir {l}'.format(l=location))
            os.system('copy {i} {l}'.format(i=item,l=location))
