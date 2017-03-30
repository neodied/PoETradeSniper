import requests
# import json
import time
from enum import Enum

CHANGE_URL = 'http://api.poe.ninja/api/Data/GetStats'
POE_API = 'http://www.pathofexile.com/api/public-stash-tabs'

sample_ES_body_armour = {
                    "verified": False,
                    "w": 2,
                    "h": 3,
                    "ilvl": 85,
                    "icon": "http://web.poecdn.com/image/Art/2DItems/Armours/BodyArmours/BodyStrDexInt1C.png?scale=1&w=2&h=3&v=5a4eb9d863bef835aa3d9cc9224f51a53",
                    "league": "Legacy",
                    "id": "23a16eea8b41c3748984eeeffef8860397ab41f893e24f390bd3750adb888711",
                    "sockets": [
                        {
                            "group": 0,
                            "attr": "I"
                        },
                        {
                            "group": 1,
                            "attr": "I"
                        }
                    ],
                    "name": "",
                    "typeLine": "<<set:MS>><<set:M>><<set:S>>Glowing Vaal Regalia of the Walrus",
                    "identified": True,
                    "corrupted": False,
                    "lockedToCharacter": False,
                    "properties": [
                        {
                            "name": "Quality",
                            "values": [
                                [
                                    "+9%",
                                    1
                                ]
                            ],
                            "displayMode": 0,
                            "type": 6
                        },
                        {
                            "name": "Energy Shield",
                            "values": [
                                [
                                    "207",
                                    1
                                ]
                            ],
                            "displayMode": 0,
                            "type": 18
                        }
                    ],
                    "requirements": [
                        {
                            "name": "Level",
                            "values": [
                                [
                                    "68",
                                    0
                                ]
                            ],
                            "displayMode": 0
                        },
                        {
                            "name": "Int",
                            "values": [
                                [
                                    "194",
                                    0
                                ]
                            ],
                            "displayMode": 1
                        }
                    ],
                    "explicitMods": [
                        "+15 to maximum Energy Shield",
                        "+34% to Cold Resistance"
                    ],
                    "frameType": 1,
                    "x": 3,
                    "y": 0,
                    "inventoryId": "Stash21",
                    "socketedItems": []
                }

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


body_armour_max_rolls = {"total armour": 2935,
                         "total evasion": 2849,
                         "total ES": 986,
                         "plus strength": 55,
                         "plus dexterity": 55,
                         "plus intelligence": 55,
                         "plus max mana": 73,
                         "plus max life": 119,
                         "plus chaos res": 35,
                         "total ele res": 144,
                         "plus life regen": 7,
                         "reduced req": 32,
                         "stun recovery": 45,
                         "phys reflect": 50}


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


def parse_property(prop_str=""):
    if prop_str.startswith("Reflects"):
        return "phys reflect", prop_str.split()[1]
    elif prop_str.endswith("% increased Energy Shield"):
        return "pct inc ES", prop_str.split("%")[0]
    elif prop_str.endswith("to maximum Energy Shield"):
        return "plus max ES", prop_str.lstrip("+").split()[0]
    elif prop_str.endswith("to maximum Life"):
        return "plus max life", prop_str.lstrip("+").split()[0]
    elif prop_str.endswith("to maximum Mana"):
        return "plus max mana", prop_str.lstrip("+").split()[0]
    elif prop_str.endswith("% to Chaos Resistance"):
        return "plus chaos res", prop_str.lstrip("+").split("%")[0]
    elif prop_str.endswith("% to Cold Resistance"):
        return "plus cold res", prop_str.lstrip("+").split("%")[0]
    elif prop_str.endswith("% to Fire Resistance"):
        return "plus fire res", prop_str.lstrip("+").split("%")[0]
    elif prop_str.endswith("% to Lightning Resistance"):
        return "plus light res", prop_str.lstrip("+").split("%")[0]
    elif prop_str.endswith("to Intelligence"):
        return "plus int", prop_str.lstrip("+").split()[0]
    elif prop_str.endswith("Life Regenerated per second"):
        return "plus life regen", prop_str.split()[0]
    elif prop_str.endswith("reduced Attribute Requirements"):
        return "reduced req", prop_str.split("%")[0]
    elif prop_str.endswith("increased Stun and Block Recovery"):
        return "stun recovery", prop_str.split("%")[0]
    else:
        print("Unknown property: {}".format(prop_str))
        return None, None


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
