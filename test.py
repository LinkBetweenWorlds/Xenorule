import json
import requests


saveOne = {'name': 'Blink', 'level': 16, 'exp': 0, 'type_class': 'mage', 'health': 10, 'health_max': 10, 'mp': 5,
           'mp_max': 5, 'damage': 1, 'defense': 0, 'wood': 147, 'stone': 233, 'iron_ore': 0, 'iron': 80, 'gold_ore': 95,
           'gold': 0, 'money': 2640, 'weapon': 'wand', 'weapon_inventory': ['wand'], 'armor': 'none',
           'armor_inventory': [],
           'inventory': {'small_health_potions': 3, 'medium_health_potions': 3, 'large_health_potions': 5,
                         'max_health_potions': 0, 'small_mp_potions': 3, 'medium_mp_potions': 4, 'large_mp_potions': 0,
                         'max_mp_potions': 4}, 'world': 'Green Field', 'quests_completed': [], 'current_quest': 'none'}


# with open('saveOneData.json', 'w') as outfile:
#    saveOneJson = json.dumps(saveOne)
#    json.dump(saveOneJson, outfile)

# with open('saveOneData.json') as json_file:
#    data = json.load(json_file)
#    saveOne = json.loads(data)
