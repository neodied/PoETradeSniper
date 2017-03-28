import requests
# import json
import time

CHANGE_URL = 'http://api.poe.ninja/api/Data/GetStats'
POE_API = 'http://www.pathofexile.com/api/public-stash-tabs'


def get_latest_change_id():
    r = requests.get(CHANGE_URL)
    return r.json()['nextChangeId']


def flag_interesting_item(item):
    if item['typeLine'] == 'Hubris' and 'note' in item:
        return True
    else:
        return False


def format_item(item, stash):
    return "[{}]{}\t{}\t{}".format(time.strftime('%H:%M:%S'), item["typeLine"], item["note"],
                                   stash["lastCharacterName"], )


def main():
    print('Grabbing latest Change ID from poe.ninja')
    change_id = get_latest_change_id()
    print('Starting Item search starting at {}'.format(change_id))

    while True:
        start_time = time.time()
        try:
            r = requests.get('{}/?id={}.gz'.format(POE_API, change_id))
            # print(change_id)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            print(str(e))
        else:
            j = r.json()
            size = len(r.content)

        change_id = j['next_change_id']

        download_time = round(time.time() - start_time, 3)
        download_rate = round(size/download_time/10**6, 3)

        for stash in j['stashes']:
            for item in stash['items']:
                if flag_interesting_item(item):
                    print(format_item(item, stash))

        end_time = round(time.time() - start_time - download_time, 3)

        print('Download {}s; Processing {}s; Download rate {}MB/s'.format(download_time, end_time, download_rate))

        if (end_time + download_time) < 1.0:
            time.sleep(1.0 - (end_time + download_time))


main()
