import json
import requests

saveOne = {'name': 'Blink', 'level': 16, 'exp': 0, 'type_class': 'mage', 'health': 10, 'health_max': 10, 'mp': 5,
           'mp_max': 5, 'damage': 1, 'defense': 0, 'wood': 147, 'stone': 233, 'iron_ore': 0, 'iron': 80, 'gold_ore': 95,
           'gold': 0, 'money': 2640, 'weapon': 'wand', 'weapon_inventory': ['wand'], 'armor': 'none',
           'armor_inventory': [],
           'inventory': {'small_health_potions': 3, 'medium_health_potions': 3, 'large_health_potions': 5,
                         'max_health_potions': 0, 'small_mp_potions': 3, 'medium_mp_potions': 4, 'large_mp_potions': 0,
                         'max_mp_potions': 4}, 'world': 'Green Field', 'quests_completed': [], 'current_quest': 'none'}


def dataStuff():
    enemyList = {
        'Green Field': ['greenSlime', 'greenSlime', 'bat', 'bat', 'zombie'],
        'greenSlime': {
            'name': 'Green Slime',
            'hp': 5,
            'element': 'normal',
            'damage_min': 1,
            'damage_max': 2,
            'defense': 0,
            'money_min': 1,
            'money_max': 4,
            'exp_min': 1,
            'exp_max': 3,
            'item_drop': ['small_health_pot', 'small_mp_pot']
        },
        'bat': {
            'name': 'Bat',
            'hp': 3,
            'element': 'flying',
            'damage_min': 1,
            'damage_max': 2,
            'defense': 0,
            'money_min': 1,
            'money_max': 2,
            'exp_min': 1,
            'exp_max': 2,
            'item_drop': ['small_health_pot', 'small_mp_pot']
        },
        'zombie': {
            'name': 'Zombie',
            'hp': 8,
            'element': 'normal',
            'damage_min': 2,
            'damage_max': 3,
            'defense': 0,
            'money_min': 2,
            'money_max': 6,
            'exp_min': 2,
            'exp_max': 4,
            'item_drop': ['small_health_pot', 'small_mp_pot']
        }
    }

    with open('gameData/enemyData.json', 'w') as outfile:
        enemyDataJson = json.dumps(enemyList)
        json.dump(enemyDataJson, outfile)
# with open('saveOneData.json', 'w') as outfile:
#    saveOneJson = json.dumps(saveOne)
#    json.dump(saveOneJson, outfile)

# with open('saveOneData.json') as json_file:
#    data = json.load(json_file)
#    saveOne = json.loads(data)
