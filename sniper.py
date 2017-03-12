import requests
import json

CHANGE_URL = 'http://api.poe.ninja/api/Data/GetStats'
POE_API = 'http://www.pathofexile.com/api/public-stash-tabs'

def getLastestChangeID():
    r = requests.get(CHANGE_URL)
    return r.json()['nextChangeId']

def filter(item):
    if(item['typeLine'] == 'Hubris' and 'note' in item):
        return True
    else:
        return False

def formatItem(item, stash):
    return "{}\t{}\t{}\t{}".format(item["note"], stash["accountName"], stash["lastCharacterName"], item["league"])


changeId = getLastestChangeID();

while True:
    try:
        r = requests.get('{}/?id={}.gz'.format(POE_API, changeId))

        print(changeId)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print(str(e))

    j = r.json()
    changeId = j['next_change_id']

    for stash in j['stashes']:
        for item in stash['items']:
            if(filter(item)):
                print(formatItem(item, stash))
