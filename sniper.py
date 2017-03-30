import requests
# import json
import time
from enum import Enum

CHANGE_URL = 'http://api.poe.ninja/api/Data/GetStats'
POE_API = 'http://www.pathofexile.com/api/public-stash-tabs'


body_armour_bases = {"Plate Vest",
                     "Chestplate",
                     "Copper Plate",
                     "War Plate",
                     "Full Plate",
                     "Arena Plate",
                     "Lordly Plate",
                     "Bronze Plate",
                     "Battle Plate",
                     "Sun Plate",
                     "Colosseum Plate",
                     "Majestic Plate",
                     "Golden Plate",
                     "Crusader Plate",
                     "Astral Plate",
                     "Gladiator Plate",
                     "Glorious Plate",
                     "Kaom's Plate",
                     "Shabby Jerkin",
                     "Strapped Leather",
                     "Buckskin Tunic",
                     "Wild Leather",
                     "Full Leather",
                     "Sun Leather",
                     "Thief's Garb",
                     "Eelskin Tunic",
                     "Frontier Leather",
                     "Glorious Leather",
                     "Coronal Leather",
                     "Cutthroat's Garb",
                     "Sharkskin Tunic",
                     "Destiny Leather",
                     "Exquisite Leather",
                     "Zodiac Leather",
                     "Assassin's Garb",
                     "Simple Robe",
                     "Silken Vest",
                     "Scholar's Robe",
                     "Silken Garb",
                     "Mage's Vestment",
                     "Silk Robe",
                     "Cabalist Regalia",
                     "Sage's Robe",
                     "Silken Wrap",
                     "Conjurer's Vestment",
                     "Spidersilk Robe",
                     "Destroyer Regalia",
                     "Savant's Robe",
                     "Necromancer Silks",
                     "Occultist's Vestment",
                     "Widowsilk Robe",
                     "Vaal Regalia",
                     "Scale Vest",
                     "Light Brigandine",
                     "Scale Doublet",
                     "Infantry Brigandine",
                     "Full Scale Armour",
                     "Soldier's Brigandine",
                     "Field Lamellar",
                     "Wyrmscale Doublet",
                     "Hussar Brigandine",
                     "Full Wyrmscale",
                     "Commander's Brigandine",
                     "Battle Lamellar",
                     "Dragonscale Doublet",
                     "Desert Brigandine",
                     "Full Dragonscale",
                     "General's Brigandine",
                     "Triumphant Lamellar",
                     "Chainmail Vest",
                     "Chainmail Tunic",
                     "Ringmail Coat",
                     "Chainmail Doublet",
                     "Full Ringmail",
                     "Full Chainmail",
                     "Holy Chainmail",
                     "Latticed Ringmail",
                     "Crusader Chainmail",
                     "Ornate Ringmail",
                     "Chain Hauberk",
                     "Devout Chainmail",
                     "Loricated Ringmail",
                     "Conquest Chainmail",
                     "Elegant Ringmail",
                     "Saint's Hauberk",
                     "Saintly Chainmail",
                     "Padded Vest",
                     "Oiled Vest",
                     "Padded Jacket",
                     "Oiled Coat",
                     "Scarlet Raiment",
                     "Waxed Garb",
                     "Bone Armour",
                     "Quilted Jacket",
                     "Sleek Coat",
                     "Crimson Raiment",
                     "Lacquered Garb",
                     "Crypt Armour",
                     "Sentinel Jacket",
                     "Varnished Coat",
                     "Blood Raiment",
                     "Sadist Garb",
                     "Carnal Armour",
                     "Sacrificial Garb",
                     "Golden Mantle"}


class FrameType(Enum):
    normal = 0
    magic = 1
    rare = 2
    unique = 3
    gem = 4
    currency = 5
    divination_card = 6
    quest_item = 7
    prophecy = 8
    relic = 9


def get_latest_change_id():
    r = requests.get(CHANGE_URL)
    return r.json()['nextChangeId']


def flag_interesting_item(item):
    if item['typeLine'] == 'Hubris' and 'note' in item:
        return True
    elif FrameType(item['frameType']) in [FrameType.normal, FrameType.magic, FrameType.rare]:
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
        download_rate = round(size / download_time / 10 ** 6, 3)

        for stash in j['stashes']:
            for item in stash['items']:
                if flag_interesting_item(item):
                    print(format_item(item, stash))

        end_time = round(time.time() - start_time - download_time, 3)

        print('Download {}s; Processing {}s; Download rate {}MB/s'.format(download_time, end_time, download_rate))

        if (end_time + download_time) < 1.0:
            time.sleep(1.0 - (end_time + download_time))


main()
