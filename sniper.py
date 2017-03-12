import requests
import json
import time

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
    return "[{}]{}\t{}\t{}\t{}".format(time.strftime('%l:%M%p %Z on %b %d, %Y'),item["note"], stash["accountName"], stash["lastCharacterName"], item["league"])



print('Grabbing latest Change ID from poe.ninja')
changeId = getLastestChangeID();
print('Starting Item search starting at {}'.format(changeId))

while True:
    start_time = time.time()
    try:
        r = requests.get('{}/?id={}.gz'.format(POE_API, changeId))
        #print(changeId)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print(str(e))

    j = r.json()
    changeId = j['next_change_id']

    download_time = time.time() - start_time

    for stash in j['stashes']:
        for item in stash['items']:
            if(filter(item)):
                print(formatItem(item, stash))

    end_time = time.time() - start_time - download_time

    print('Download took {}s; Processing took {}s'.format(download_time, end_time))
    if((end_time + download_time) < 1.0 ) time.sleep(1.0 - (end_time + download_time))
