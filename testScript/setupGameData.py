import json


def playerDataUpdate():
    saveOverride = {'name': 'Empty', 'type_class': 'none', 'level': 0, 'exp': 0}
    saveOverrideJson = json.dumps(saveOverride)

    with open('playerData/saveOneData.json', 'w') as outfile:
        json.dump(saveOverrideJson, outfile)
    with open('playerData/saveTwoData.json', 'w') as outfile:
        json.dump(saveOverrideJson, outfile)
    with open('playerData/saveThreeData.json', 'w') as outfile:
        json.dump(saveOverrideJson, outfile)


def settingsDataUpdate():
    settings = {
        'backgroundMusic': True,
        'soundFX': True,
        'fullscreen': True,
        'textSpeed': 0.01,
        'width': 1280,
        'height': 720
    }

    with open('gameData/settings.json', 'w') as outfile:
        settingsJson = json.dumps(settings)
        json.dump(settingsJson, outfile)


def battleDataUpdate():
    battleData = {
        'current_enemy': 'none',
        'currently_fighting': False,
        'current_enemy_data': {},
        'current_enemy_health': 0,
        'turn_count': 0
    }

    with open('gameData/battleData.json', 'w') as outfile:
        battleDataJson = json.dumps(battleData)
        json.dump(battleDataJson, outfile)


def enemyDataUpdate():
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


def attackDataUpdate():
    attack_lists = {
        'mage_attack_list': {
            'attack': {
                'name': 'Attack',
                'damage': 1,
                'element': 'normal',
                'mp_cost': 0,
                'piercing': False
            },
            'fire_attack': {
                'name': 'Fire Blast',
                'damage': 2,
                'element': 'fire',
                'mp_cost': 1,
                'piercing': False
            }
        },
        'paladin_attack_list': {
            'attack': {
                'name': 'Attack',
                'damage': 1,
                'element': 'normal',
                'mp_cost': 0,
                'piercing': False
            },
            'fire_attack': {
                'name': 'Fire Swing',
                'damage': 2,
                'element': 'fire',
                'mp_cost': 1,
                'piercing': False
            }
        },
        'archer_attack_list': {
            'attack': {
                'name': 'Attack',
                'damage': 1,
                'element': 'normal',
                'mp_cost': 0,
                'piercing': False
            },
            'fire_attack': {
                'name': 'Fire Bolt',
                'damage': 2,
                'element': 'fire',
                'mp_cost': 1,
                'piercing': False
            }
        }
    }


    with open('gameData/attackData.json', 'w') as outfile:
        attacksJson = json.dumps(attack_lists)
        json.dump(attacksJson, outfile)

def allDataUpdate():
    attackDataUpdate()
    enemyDataUpdate()
    playerDataUpdate()
    battleDataUpdate()
    settingsDataUpdate()

battleDataUpdate()