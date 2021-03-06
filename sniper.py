import requests
import time
import numpy as np

CHANGE_URL = 'http://api.poe.ninja/api/Data/GetStats'
POE_API = 'http://www.pathofexile.com/api/public-stash-tabs'

TYPE_normal = 0
TYPE_magic = 1
TYPE_rare = 2
TYPE_unique = 3
TYPE_gem = 4
TYPE_currency = 5
TYPE_divination_card = 6
TYPE_quest_item = 7
TYPE_prophecy = 8
TYPE_relic = 9

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

body_armour_max_rolls = {"total AR": 2935,
                         "total EV": 2849,
                         "total ES": 986,
                         "plus str": 55,
                         "plus dex": 55,
                         "plus int": 55,
                         "plus max mana": 73,
                         "plus max life": 119,
                         "plus chaos res": 35,
                         "total ele res": 144,
                         "plus life regen": 7,
                         "reduced req": 32,
                         "stun recovery": 45,
                         "phys reflect": 50}

body_armour_prop_vector = ("total AR",
                           "total EV",
                           "total ES",
                           "plus str",
                           "plus dex",
                           "plus int",
                           "plus max mana",
                           "plus max life",
                           "plus chaos res",
                           "total ele res",
                           "plus life regen",
                           "reduced req",
                           "stun recovery",
                           "phys reflect")


def calc_synergy_score(perfection_list):
    size = len(body_armour_prop_vector)
    a = np.ones((size, 1))
    b = np.array(perfection_list)[np.newaxis]

    perfection_cols = np.dot(a, b)
    perfection_rows = perfection_cols.transpose()
    perfection_sum = perfection_cols + perfection_rows + np.ones(perfection_cols.shape)
    lower_tri = np.tril(perfection_sum)

    try:
        synergy_power = np.genfromtxt("synergy_table.txt", delimiter="\t")
    except:
        raise
    else:
        powered_tri = np.power(lower_tri, synergy_power) - np.ones((size, size))
        score = int(round(np.sum(powered_tri)))

    return score


def parse_raw_mod(prop_str=""):
    if prop_str.startswith("Reflects"):
        return "phys reflect", int(prop_str.split()[1])
    elif prop_str.endswith("% increased Armour"):
        return "pct inc AR", int(prop_str.split("%")[0])
    elif prop_str.endswith("% increased Evasion Rating"):
        return "pct inc EV", int(prop_str.split("%")[0])
    elif prop_str.endswith("% increased Energy Shield"):
        return "pct inc ES", int(prop_str.split("%")[0])
    elif prop_str.endswith("% increased Armour and Evasion"):
        return "pct inc AR+EV", int(prop_str.split("%")[0])
    elif prop_str.endswith("% increased Armour and Energy Shield"):
        return "pct inc AR+ES", int(prop_str.split("%")[0])
    elif prop_str.endswith("% increased Evasion and Energy Shield"):
        return "pct inc EV+ES", int(prop_str.split("%")[0])
    elif prop_str.endswith("to Armour"):
        return "plus max ES", int(prop_str.lstrip("+").split()[0])
    elif prop_str.endswith("to Evasion Rating"):
        return "plus max ES", int(prop_str.lstrip("+").split()[0])
    elif prop_str.endswith("to maximum Energy Shield"):
        return "plus max ES", int(prop_str.lstrip("+").split()[0])
    elif prop_str.endswith("to maximum Life"):
        return "plus max life", int(prop_str.lstrip("+").split()[0])
    elif prop_str.endswith("to maximum Mana"):
        return "plus max mana", int(prop_str.lstrip("+").split()[0])
    elif prop_str.endswith("% to Chaos Resistance"):
        return "plus chaos res", int(prop_str.lstrip("+").split("%")[0])
    elif prop_str.endswith("% to Cold Resistance"):
        return "plus cold res", int(prop_str.lstrip("+").split("%")[0])
    elif prop_str.endswith("% to Fire Resistance"):
        return "plus fire res", int(prop_str.lstrip("+").split("%")[0])
    elif prop_str.endswith("% to Lightning Resistance"):
        return "plus light res", int(prop_str.lstrip("+").split("%")[0])
    elif prop_str.endswith("% to all Elemental Resistances"):
        return "plus all res", int(prop_str.lstrip("+").split("%")[0])
    elif prop_str.endswith("to Strength"):
        return "plus str", int(prop_str.lstrip("+").split()[0])
    elif prop_str.endswith("to Dexterity"):
        return "plus dex", int(prop_str.lstrip("+").split()[0])
    elif prop_str.endswith("to Intelligence"):
        return "plus int", int(prop_str.lstrip("+").split()[0])
    elif prop_str.endswith("Life Regenerated per second"):
        return "plus life regen", float(prop_str.split()[0])
    elif prop_str.endswith("reduced Attribute Requirements"):
        return "reduced req", int(prop_str.split("%")[0])
    elif prop_str.endswith("increased Stun and Block Recovery"):
        return "stun recovery", int(prop_str.split("%")[0])
    elif prop_str == "3% increased Movement Speed":
        return None, None
    else:
        print("Unknown property: {}".format(prop_str))
        return None, None


def calc_summary_stats(raw_item):
    AR = 0
    EV = 0
    ES = 0
    if "properties" in raw_item:
        for prop in raw_item["properties"]:
            if prop["name"] == "Armour":
                AR = int(prop["values"][0][0])
            elif prop["name"] == "Evasion":
                EV = int(prop["values"][0][0])
            elif prop["name"] == "Energy Shield":
                ES = int(prop["values"][0][0])

    combined_mods = raw_item["explicitMods"] if "explicitMods" in raw_item else []
    combined_mods = combined_mods + raw_item["implicitMods"] if "implicitMods" in raw_item else combined_mods

    parsed_mods = dict([parse_raw_mod(mod) for mod in combined_mods])

    total_ele_res = parsed_mods["plus all res"] if "plus all res" in parsed_mods else 0
    total_ele_res = total_ele_res + parsed_mods["plus cold res"] if "plus cold res" in parsed_mods else total_ele_res
    total_ele_res = total_ele_res + parsed_mods["plus fire res"] if "plus fire res" in parsed_mods else total_ele_res
    total_ele_res = total_ele_res + parsed_mods["plus light res"] if "plus light res" in parsed_mods else total_ele_res

    summary_stats = parsed_mods
    summary_stats["total AR"] = AR
    summary_stats["total EV"] = EV
    summary_stats["total ES"] = ES
    summary_stats["total ele res"] = total_ele_res

    return summary_stats


def calc_perfection_vector(summary_stats):
    perfection = []
    for prop in body_armour_prop_vector:
        try:
            perfection.append(summary_stats[prop] / body_armour_max_rolls[prop])
        except KeyError:
            perfection.append(0)
    return perfection


def get_latest_change_id():
    r = requests.get(CHANGE_URL)
    return r.json()['nextChangeId']


def flag_interesting_item(item):
    if item['frameType'] in [TYPE_normal, TYPE_magic, TYPE_rare] and item['typeLine'] in body_armour_bases:
        summary = calc_summary_stats(item)
        perfection_vector = calc_perfection_vector(summary)
        score = calc_synergy_score(perfection_vector)
        return score, summary
    else:
        return False, None


def notify_item(item, stash):
    return "[{}]{}\t{}\t{}".format(time.strftime('%H:%M:%S'), item["typeLine"], item["note"] if "note" in item else "",
                                   stash["lastCharacterName"], )


def output(item, score, prop_summary):
    props_line = ','.join(['{}:{}'.format(k, v) for k, v in prop_summary.items()])
    return "\t".join([item["id"], item["typeLine"], str(score), props_line])


def main():
    print('Grabbing latest Change ID from poe.ninja')
    change_id = get_latest_change_id()
    print('Starting Item search starting at {}'.format(change_id))

    while True:
        start_time = time.time()
        try:
            r = requests.get('{}/?id={}.gz'.format(POE_API, change_id))
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

        with open("scored_items.log", 'a') as outfile:
            for stash in j['stashes']:
                for item in stash['items']:
                    score_summary = flag_interesting_item(item)
                    if score_summary[0]:
                        s = output(item, score_summary[0], score_summary[1])
                        print(s)
                        outfile.write(s+'\n')

        end_time = round(time.time() - start_time - download_time, 3)

        print('Download {}s; Processing {}s; Download rate {}MB/s'.format(download_time, end_time, download_rate))

        if (end_time + download_time) < 1.0:
            time.sleep(1.0 - (end_time + download_time))


main()
