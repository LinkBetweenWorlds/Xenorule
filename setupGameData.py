import json


def resetPlayerData():
    playerSave = {'name': 'Empty', 'level': 0, 'exp': 0, 'type_class': 'none'}
    playerSaveJson = json.dumps(playerSave)
    with open('playerData/saveOneData.json', 'w') as outfile:
        json.dump(playerSaveJson, outfile)
    with open('playerData/saveTwoData.json', 'w') as outfile:
        json.dump(playerSaveJson, outfile)
    with open('playerData/saveThreeData.json', 'w') as outfile:
        json.dump(playerSaveJson, outfile)


def saveGameData():

    settingsData = {'backgroundMusic': False, 'soundFX': False}
    battleData = {'current_enemy': 'none', 'currently_fighting': False, 'current_enemy_health': 0, 'turn_count': 0}

    saveSettingsJson = json.dumps(settingsData)
    battleDataJson = json.dumps(battleData)

    with open('gameData/settings.json', 'w') as outfile:
        json.dump(saveSettingsJson, outfile)
    with open('gameData/battleData.json', 'w') as outfile:
        json.dump(battleDataJson, outfile)

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


saveGameData()
resetPlayerData()