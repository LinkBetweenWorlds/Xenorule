import json
import math
import multiprocessing
import os.path
import random
from tkinter import *
from PIL import Image, ImageTk
import asynctkinter as at
import time
from threading import *

# Setup game window
window = Tk()
window.title('Xenorule')
window.configure(background='black')
window.geometry('1280x720')
window.resizable(width=NO, height=NO)
window.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('appicon.gif')))

# Setup text box
playerStatsOutput = Text(window, width=60, height=10, bg='black', fg='white', font='times 16')
playerStatsOutput.grid(row=0, column=0, sticky='w')
playerStatsOutput.configure(state='disabled')
playerEquipOutput = Text(window, width=60, height=10, bg='black', fg='white', font='times 16')
playerEquipOutput.grid(row=0, column=1, sticky='w')
playerEquipOutput.configure(state='disabled')
textOutput = Text(window, width=120, height=13, bg='black', fg='white', font='times 16')
textOutput.grid(row=1, column=0, columnspan=2, sticky='w')
textOutput.configure(state='disabled')
Label(window, text='Answer:', bg='black', fg='white', font='times 16').grid(row=2, column=0, sticky='w')
playerAnswerBox = Entry(window, width=120, bg='black', fg='white', font='times 16')
playerAnswerBox.grid(row=3, column=0, columnspan=2, sticky='w')

slotNumber = 0
playerData = {}
all_processes = []


async def startGame():
    if os.path.exists('playerData/saveOneData.json'):
        loadData()
        text = 'Welcome to Xenorule!\n'
        text += 'What would you like to do?\n\n'
        text += '1. Play\n'
        text += '2. Erase\n'
        text += '3. Settings\n'
        text += '4. Exit\n'
        text += 'Answer: 1, 2, 3, 4'
        options = ['play', 'erase', 'settings', 'exit', '1', '2', '3', '4']
        playerButton['text'] = 'Submit'
        setTextOutput(text)
        await at.event(playerButton, '<Button>')
        answer = grabText()
        if options.__contains__(answer):
            if answer == 'play' or answer == '1':
                at.start(playerSelect())
            if answer == 'erase' or answer == '2':
                at.start(erasePlayer())
            if answer == 'settings' or answer == '3':
                at.start(settings())
            if answer == 'exit' or answer == '4':
                exitGame()
        else:
            text = 'That is not an option.'
            playerButton['text'] = 'Next'
            setTextOutput(text)
            await at.event(playerButton, '<Button>')
            at.start(startGame())
    else:
        firstTimeStartUp()


async def newGame():
    global playerData
    global slotNumber
    text = 'Welcome to Xenorule!\n'
    text += 'What is your name, traveller?'
    playerButton['text'] = 'Submit'
    setTextOutput(text)
    await at.event(playerButton, '<Button>')
    answer = playerAnswerBox.get()
    playerAnswerBox.delete(0, END)
    playerData['name'] = answer
    playerData['level'] = 1
    playerData['exp'] = 0
    playerData['type_class'] = 'none'
    playerData['health'] = 10
    playerData['health_max'] = 10
    playerData['mp'] = 5
    playerData['mp_max'] = 5
    playerData['damage'] = 1
    playerData['defense'] = 0
    playerData['attacks'] = {
        'attack_list': [],
        'attack_damage': []
    }
    playerData['wood'] = 0
    playerData['stone'] = 0
    playerData['iron_ore'] = 0
    playerData['iron'] = 0
    playerData['gold_ore'] = 0
    playerData['gold'] = 0
    playerData['money'] = 0
    playerData['weapon'] = 'none'
    playerData['weapon_inventory'] = []
    playerData['armor'] = 'none'
    playerData['armor_inventory'] = []
    playerData['inventory'] = {
        'small_health_potions': 0,
        'medium_health_potions': 0,
        'large_health_potions': 0,
        'max_health_potions': 0,
        'small_mp_potions': 0,
        'medium_mp_potions': 0,
        'large_mp_potions': 0,
        'max_mp_potions': 0
    }
    playerData['world'] = 'Green Field'
    playerData['quests_completed'] = []
    playerData['current_quest'] = 'none'
    text = 'Welcome ' + answer + ', are you ready for your adventure to begin!'
    saveData()
    setTextOutput(text)
    playerButton['text'] = 'Next'
    await at.event(playerButton, '<Button>')
    at.start(chooseClass())


def firstTimeStartUp():
    saveOverride = {'name': 'Empty', 'type_class': 'none', 'level': 0, 'exp': 0}
    saveOverrideJson = json.dumps(saveOverride)
    os.mkdir("./playerData")

    with open('playerData/saveOneData.json', 'w') as outfile:
        json.dump(saveOverrideJson, outfile)
    with open('playerData/saveTwoData.json', 'w') as outfile:
        json.dump(saveOverrideJson, outfile)
    with open('playerData/saveThreeData.json', 'w') as outfile:
        json.dump(saveOverrideJson, outfile)

    at.start(startGame())


async def playerSelect():
    loadData()
    global playerData
    global slotNumber
    text = 'What save would you like to use?\n\n'
    text += '1. ' + saveOne['name'] + '\n'
    text += '2. ' + saveTwo['name'] + '\n'
    text += '3. ' + saveThree['name'] + '\n'
    text += '4. Back\n'
    text += 'Answer: 1, 2, 3, 4'
    options = ['1', '2', '3', '4']
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == '1':
            playerData = saveOne
            slotNumber = 1
            if playerData['name'] == 'Empty':
                at.start(newGame())
            else:
                if playerData['type_class'] == 'none':
                    at.start(chooseClass())
                else:
                    at.start(gameLoop())
        if answer == '2':
            playerData = saveTwo
            slotNumber = 2
            if playerData['name'] == 'Empty':
                at.start(newGame())
            else:
                if playerData['type_class'] == 'none':
                    at.start(chooseClass())
                else:
                    at.start(gameLoop())
        if answer == '3':
            playerData = saveThree
            slotNumber = 3
            if playerData['name'] == 'Empty':
                at.start(newGame())
            else:
                if playerData['type_class'] == 'none':
                    at.start(chooseClass())
                else:
                    at.start(gameLoop())
        if answer == '4':
            at.start(startGame())
    else:
        text = 'That is not an answer.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(startGame())


async def settings():
    global settingsData
    textSpeed = settingsData['textSpeed']
    textSpeedWord = ''
    if textSpeed == 0:
        textSpeedWord = 'Instant'
    elif textSpeed == 0.01:
        textSpeedWord = 'Fast'
    elif textSpeed == 0.03:
        textSpeedWord = 'Normal'
    elif textSpeed == 0.05:
        textSpeedWord = 'Slow'
    text = 'Settings\n'
    text += '1. Background Music: ' + str(settingsData['backgroundMusic']) + '\n'
    text += '2. Sound FX: ' + str(settingsData['soundFX']) + '\n'
    text += '3. Screen Size\n'
    text += '4. Text Speed: ' + textSpeedWord + '\n'
    text += '5. Back\n'
    text += 'What settings would you like to change. (1, 2, 3, 4, 5)'
    playerButton['text'] = 'Submit'
    setTextOutput(text)
    options = ['1', '2', '3', '4', '5', 'backgroundmusic', 'soundfx', 'screensize', 'textspeed', 'back']
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == '1' or answer == 'backgroundmusic':
            settingsData['backgroundMusic'] = not settingsData['backgroundMusic']
            saveData()
            at.start(settings())
        if answer == '2' or answer == 'soundfx':
            settingsData['soundFX'] = not settingsData['soundFX']
            saveData()
            at.start(settings())
        if answer == '3' or answer == 'screensize':
            at.start(screenOptions())
        if answer == '4' or answer == 'textspeed':
            at.start(textSpeedOptions())
        if answer == '5' or answer == 'back':
            at.start(startGame())
    else:
        text = 'That is not an option.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(settings())


async def screenOptions():
    # TODO work out how to do this
    global settingsData
    text = 'Which settings would you like to change.\n\n'
    text += '1. Fullscreen: ' + str(settingsData['fullscreen']) + '\n'
    text += '2. Screen Size: ' + str(settingsData['width']) + ' x ' + str(settingsData['height']) + '\n'
    text += '3. Back'
    setTextOutput(text)
    options = ['1', '2', '3', 'fullscreen', 'screensize', 'back']
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == '1' or answer == 'fullscreen':
            settingsData['fullscreen'] = not settingsData['fullscreen']
            window.attributes('-fullscreen', settingsData['fullscreen'])
            saveData()
            at.start(screenOptions())
        if answer == '2' or answer == 'screensize':
            screenSizeOptions = ['1980x1080', '1280x720']
    else:
        text = 'That is not an option.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(screenOptions())


async def textSpeedOptions():
    global settingsData

    text = 'What speed would you like to change to?\n\n'
    text += '1. Instant\n'
    text += '2. Fast\n'
    text += '3. Normal\n'
    text += '4. Slow\n'
    text += '5. Back'
    options = ['1', '2', '3', '4', '5', 'instant', 'fast', 'normal', 'slow', 'back']
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == '1' or answer == 'instant':
            settingsData['textSpeed'] = 0
        if answer == '2' or answer == 'fast':
            settingsData['textSpeed'] = 0.01
        if answer == '3' or answer == 'normal':
            settingsData['textSpeed'] = 0.03
        if answer == '4' or answer == 'slow':
            settingsData['textSpeed'] = 0.05
        if answer == '5' or answer == 'back':
            at.start(settings())
        saveData()
        at.start(settings())
    else:
        text = 'That is not an option.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(textSpeedOptions())


async def chooseClass():
    global playerData
    global attackData

    text = 'What class would you like to be?\n\n'
    text += '1. Mage: Casts powerful spells to defeat their enemies.\n'
    text += '2. Paladin: Slashes their enemies to pieces.\n'
    text += '3. Archer: Rains arrows down on their foes.\n'
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    options = ['mage', '1', 'paladin', '2', 'archer', '3']
    if options.__contains__(answer):
        playerButton['text'] = 'Next'
        if answer == 'mage' or answer == '1':
            text = 'You selected mage class.\n'
            text += 'You got a wand.'
            setTextOutput(text)
            playerData['type_class'] = 'mage'
            playerData['weapon'] = 'wand'
            playerData['weapon_inventory'].append(playerData['weapon'])
            playerData['attacks']['attack_list'].append(attackData['mage_attack_list']['attack'])
        if answer == 'paladin' or answer == '2':
            text = 'You have selected paladin class.\n'
            text += 'You received a sword.'
            setTextOutput(text)
            playerData['type_class'] = 'paladin'
            playerData['weapon'] = 'sword'
            playerData['weapon_inventory'].append(playerData['weapon'])
            playerData['attacks']['attack_list'].append(attackData['paladin_attack_list']['attack'])
        if answer == 'archer' or answer == '3':
            text = 'You are now an archer.\n'
            text += 'You got a bow.'
            setTextOutput(text)
            playerData['type_class'] = 'archer'
            playerData['weapon'] = 'bow'
            playerData['weapon_inventory'].append(playerData['weapon'])
            playerData['attacks']['attack_list'].append(attackData['archer_attack_list']['attack'])
        await at.event(playerButton, '<Button>')
        saveData()
        at.start(gameLoop())
    else:
        text = 'That is not an answer.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(chooseClass())


async def erasePlayer():
    global saveOne
    global saveTwo
    global saveThree
    if saveOne['name'] == 'Empty' and saveTwo['name'] == 'Empty' and saveThree['name'] == 'Empty':
        text = 'You do not have any slots to erase.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(startGame())
    else:
        text = 'Which slot would you like to erase?\n\n'
        options = ['exit']
        if saveOne['name'] != 'Empty':
            text += '1. ' + saveOne['name'] + '\n'
            options += ['1']
        if saveTwo['name'] != 'Empty':
            text += '2. ' + saveTwo['name'] + '\n'
            options += ['2']
        if saveThree['name'] != 'Empty':
            text += '3. ' + saveThree['name'] + '\n'
            options += ['3']
        text += 'Options: 1, 2, 3, back'
        setTextOutput(text)
        playerButton['text'] = 'Submit'
        await at.event(playerButton, '<Button>')
        answer = grabText()
        if options.__contains__(answer):
            if answer == 'back':
                at.start(startGame())
            else:
                text = 'Are you sure you want to erase this save slot you cannot get the data back.\n'
                text += 'Yes / No'
                setTextOutput(text)
                playerButton['text'] = 'Submit'
                await at.event(playerButton, '<Button>')
                eraseSlot = answer
                answer = grabText()
                options = ['yes', 'no']
                if options.__contains__(answer):
                    if answer == 'yes':
                        erasePlayerData(eraseSlot)
                        # await at.sleep(500, after=playerButton.after)
                        text = 'Save slot erased.'
                        setTextOutput(text)
                        playerButton['text'] = 'Next'
                        await at.event(playerButton, '<Button>')
                        at.start(startGame())
                    if answer == 'no':
                        at.start(startGame())
        else:
            text = 'That is not an option.'
            setTextOutput(text)
            playerButton['text'] = 'Next'
            await at.event(playerButton, '<Button>')
            at.start(erasePlayer())


async def gameLoop():
    global playerData

    # Update PlayerStats and equipment text
    updatePlayerStats()
    n = 0
    level = playerData['level']
    text = 'What would you like to do?\n\n'
    text += '1. Chop\n'
    text += '2. Mine\n'
    text += '3. Fight\n'
    text += '4. Heal\n'
    n += 5
    options = ['1', 'chop', '2', 'mine', '3', 'fight', '4', 'heal', 'back']
    if level >= 3:
        text += '5. Shop\n'
        options += ['shop', '5']
        n += 1
    if level >= 5:
        text += '6. Smelt\n'
        options += ['smelt', '6']
        n += 1
    if level >= 7:
        text += '7. Travel\n'
        options += ['travel', '7']
        n += 1
    if level >= 10:
        text += '8. Quests\n'
        options += ['quests', '8']
        n += 1
    if level >= 12:
        text += '9. Dojo\n'
        options += ['dojo', '9']
        n += 1
    if level >= 15:
        text += '10. Enchant\n'
        options += ['enchant', '10']
        n += 1
    text += str(n) + '. Back'
    options += [str(n)]
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == 'back' or answer == str(n):
            playerStatsOutput.configure(state='normal')
            playerEquipOutput.configure(state='normal')
            playerStatsOutput.delete(0.0, END)
            playerEquipOutput.delete(0.0, END)
            playerStatsOutput.configure(state='disabled')
            playerEquipOutput.configure(state='disabled')
            at.start(startGame())
        else:
            if answer == 'chop' or answer == '1':
                wood_gained = random.randint(2, 5) * level
                text = 'You go to the forest to chop down some trees.\n'
                text += 'You gained ' + str(wood_gained) + ' wood.'
                playerData['wood'] += wood_gained
                saveData()
                setTextOutput(text)
                playerButton['text'] = 'Next'
                await at.event(playerButton, '<Button>')
                at.start(gameLoop())
            if answer == 'mine' or answer == '2':
                iron_ore_gained = random.randint(3, 5) * level
                gold_ore_gained = random.randint(2, 3) * level
                stone_gained = random.randint(3, 4) * level
                text = 'You go to the mines to get some stones'
                if level >= 5:
                    text += ', iron and gold.\n'
                    playerData['iron_ore'] += iron_ore_gained
                    playerData['gold_ore'] += gold_ore_gained
                else:
                    text += '.\n'
                playerData['stone'] += stone_gained
                text += 'You gained ' + str(stone_gained) + ' stone.\n'
                if level >= 5:
                    text += 'You gained ' + str(iron_ore_gained) + ' iron ore.\n'
                    text += 'You gained ' + str(gold_ore_gained) + ' gold ore.'
                saveData()
                setTextOutput(text)
                playerButton['text'] = 'Next'
                await at.event(playerButton, '<Button>')
                at.start(gameLoop())
            if answer == 'fight' or answer == '3':
                at.start(fight())
            if answer == 'heal' or answer == '4':
                at.start(heal())
            if answer == 'shop' or answer == '5':
                at.start(shop())
            if answer == 'smelt' or answer == '6':
                at.start(smelt())
            if answer == 'travel' or answer == '7':
                at.start(travel())
            if answer == 'quests' or answer == '8':
                at.start(quests())
            if answer == 'dojo' or answer == '9':
                at.start(dojo())
            if answer == 'enchant' or answer == '10':
                at.start(enchant())
    else:
        text = 'That is not an answer.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(gameLoop())


async def heal():
    global playerData

    if playerData['health'] == playerData['health_max'] and playerData['mp'] == playerData['mp_max']:
        text = 'You are already at max health and MP.\n'
        text += 'You have no reason to heal.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(gameLoop())
    else:
        small_health_pot = playerData['inventory']['small_health_potions']
        medium_health_pot = playerData['inventory']['medium_health_potions']
        large_health_pot = playerData['inventory']['large_health_potions']
        max_health_pot = playerData['inventory']['max_health_potions']
        total_health_pot = small_health_pot + medium_health_pot + large_health_pot + max_health_pot

        small_mp_pot = playerData['inventory']['small_mp_potions']
        medium_mp_pot = playerData['inventory']['medium_mp_potions']
        large_mp_pot = playerData['inventory']['large_mp_potions']
        max_mp_pot = playerData['inventory']['max_mp_potions']
        total_mp_pot = small_mp_pot + medium_mp_pot + large_mp_pot + max_mp_pot

        if total_mp_pot == 0 and total_health_pot == 0:
            text = 'You do not have any potions to use!\n'
            text += 'You can get them from the shop or by defeating enemies.'
            setTextOutput(text)
            playerButton['text'] = 'Next'
            await at.event(playerButton, '<Button>')
            at.start(gameLoop())
        else:
            text = 'What potion would you like to use?\n'
            options = ['exit', 'back']
            n = 1
            shp = 0
            mhp = 0
            lhp = 0
            mahp = 0
            smp = 0
            mmp = 0
            lmp = 0
            mamp = 0
            if total_health_pot > 0:
                text += '\nHealth Potions\n'
            if small_health_pot > 0:
                text += str(n) + '. Small Health Potion: x' + str(small_health_pot) + ' Restores 10 health points.\n'
                options += ['smallhealth', str(n)]
                shp = n
                n += 1
            if medium_health_pot > 0:
                text += str(n) + '. Medium Health Potion: x' + str(medium_health_pot) + ' Restores 35 health points.\n'
                options += ['mediumhealth', str(n)]
                mhp = n
                n += 1
            if large_health_pot > 0:
                text += str(n) + '. Large Health Potion: x' + str(large_health_pot) + ' Restores 70 health points.\n'
                options += ['largehealth', str(n)]
                lhp = n
                n += 1
            if max_health_pot > 0:
                text += str(n) + '. Max Health Potion: x' + str(max_health_pot) + ' Restores all your health points.\n'
                options += ['maxhealth', str(n)]
                mahp = n
                n += 1
            if total_mp_pot > 0:
                text += '\nMP Potions\n'
            if small_mp_pot > 0:
                text += str(n) + '. Small MP Potion: x' + str(small_mp_pot) + ' Restores 10 MP.\n'
                options += ['smallmp', str(n)]
                smp = n
                n += 1
            if medium_mp_pot > 0:
                text += str(n) + '. Medium MP Potion: x' + str(medium_mp_pot) + ' Restores 35 MP.\n'
                options += ['mediummp', str(n)]
                mmp = n
                n += 1
            if large_mp_pot > 0:
                text += str(n) + '. Large MP Potion: x' + str(large_mp_pot) + ' Restores 70 MP.\n'
                options += ['largemp', str(n)]
                lmp = n
                n += 1
            if max_mp_pot > 0:
                text += str(n) + '. Max MP Potion: x' + str(max_mp_pot) + ' Restores all your MP.\n'
                options += ['maxmp', str(n)]
                mamp = 0
                n += 1
            text += str(n) + '. Back'
            options += [str(n)]
            setTextOutput(text)
            playerButton['text'] = 'Submit'
            await at.event(playerButton, '<Button>')
            answer = grabText()
            if options.__contains__(answer):
                num = random.randint(1, 3)
                if answer.__contains__('smallhealth') or answer == shp:
                    if num == 1:
                        text = 'You use a small health potion and gained 10 health points.'
                    if num == 2:
                        text = 'You drank a small health potion and regenerated 10 health points.'
                    if num == 3:
                        text = 'You consumed a small health potion and got back 10 health points.'
                    setTextOutput(text)
                    playerData['health'] += 10
                    if playerData['health'] > playerData['health_max']:
                        playerData['health'] = playerData['health_max']
                    playerData['inventory']['small_health_potions'] -= 1
                    saveData()
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    at.start(gameLoop())
                if answer.__contains__('mediumhealth') or answer == mhp:
                    if num == 1:
                        text = 'You use a medium health potion and gained 35 health points.'
                    if num == 2:
                        text = 'You drank a medium health potion and regenerated 35 health points.'
                    if num == 3:
                        text = 'You consumed a medium health potion and got back 35 health points.'
                    setTextOutput(text)
                    playerData['health'] += 35
                    if playerData['health'] > playerData['health_max']:
                        playerData['health'] = playerData['health_max']
                    playerData['inventory']['medium_health_potions'] -= 1
                    saveData()
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    at.start(gameLoop())
                if answer.__contains__('largehealth') or answer == lhp:
                    if num == 1:
                        text = 'You use a large health potion and gained 70 health points.'
                    if num == 2:
                        text = 'You drank a large health potion and regenerated 70 health points.'
                    if num == 3:
                        text = 'You consumed a large health potion and got back 70 health points.'
                    setTextOutput(text)
                    playerData['health'] += 70
                    if playerData['health'] > playerData['health_max']:
                        playerData['health'] = playerData['health_max']
                    playerData['inventory']['large_health_potions'] -= 1
                    saveData()
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    at.start(gameLoop())
                if answer.__contains__('maxhealth') or answer == mahp:
                    if num == 1:
                        text = 'You use a max health potion and gained all your health points back.'
                    if num == 2:
                        text = 'You drank a max health potion and regenerated all your health points.'
                    if num == 3:
                        text = 'You consumed a max health potion and got back all your health points.'
                    setTextOutput(text)
                    playerData['health'] = playerData['health_max']
                    playerData['inventory']['max_health_potions'] -= 1
                    saveData()
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    at.start(gameLoop())
                if answer.__contains__('smallmp') or answer == smp:
                    if num == 1:
                        text = 'You use a small MP potion and gained 10 MP.'
                    if num == 2:
                        text = 'You drank a small MP potion and regenerated 10 MP.'
                    if num == 3:
                        text = 'You consumed a small MP potion and got back 10 MP.'
                    setTextOutput(text)
                    playerData['mp'] += 10
                    if playerData['mp'] > playerData['mp_max']:
                        playerData['mp'] = playerData['mp']
                    playerData['inventory']['small_mp_potions'] -= 1
                    saveData()
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    at.start(gameLoop())
                if answer.__contains__('mediummp') or answer == mmp:
                    if num == 1:
                        text = 'You use a medium MP potion and gained 35 MP.'
                    if num == 2:
                        text = 'You drank a medium MP potion and regenerated 35 MP.'
                    if num == 3:
                        text = 'You consumed a medium MP potion and got back 35 MP.'
                    setTextOutput(text)
                    playerData['mp'] += 35
                    if playerData['mp'] > playerData['mp_max']:
                        playerData['mp'] = playerData['mp_max']
                    playerData['inventory']['medium_mp_potions'] -= 1
                    saveData()
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    at.start(gameLoop())
                if answer.__contains__('largemp') or answer == lmp:
                    if num == 1:
                        text = 'You use a large MP potion and gained 70 MP.'
                    if num == 2:
                        text = 'You drank a large MP potion and regenerated 70 MP.'
                    if num == 3:
                        text = 'You consumed a large MP potion and got back 70 MP.'
                    setTextOutput(text)
                    playerData['mp'] += 70
                    if playerData['mp'] > playerData['mp_max']:
                        playerData['mp'] = playerData['mp_max']
                    playerData['inventory']['large_mp_potions'] -= 1
                    saveData()
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    at.start(gameLoop())
                if answer.__contains__('maxmp') or answer == mamp:
                    if num == 1:
                        text = 'You use a max MP potion and gained all your MP back.'
                    if num == 2:
                        text = 'You drank a max MP potion and regenerated all your MP.'
                    if num == 3:
                        text = 'You consumed a max MP potion and got back all your MP.'
                    setTextOutput(text)
                    playerData['health'] = playerData['health_max']
                    playerData['inventory']['max_health_potions'] -= 1
                    saveData()
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    at.start(gameLoop())
                if answer == 'back' or answer == str(n):
                    at.start(gameLoop())
            else:
                text = 'You do not have that potion.'
                setTextOutput(text)
                playerButton['text'] = 'Next'
                await at.event(playerButton, '<Button>')
                at.start(heal())


async def fight():
    # TODO Fight
    global playerData

    attacks = playerData['attacks']['attack_list']

    text = 'You start to fight an enemy.\n\n'
    options = []
    num = 0
    for i in attacks:
        num += 1
        text += str(num) + '. ' + i['name'] + '    MP: ' + str(i['mp_cost']) + '\n'
        options += str(num)
        options.append(i['name'])
    setTextOutput(text)
    print(options)


async def shop():
    # Buy health and MP potions
    # Sell Wood, Stone, Iron, Gold for Coins
    global playerData
    level = playerData['level']
    text = 'Welcome to the shop!\n'
    text += 'What would you like to do?\n\n'
    text += '1. Buy\n'
    options = ['back', 'buy', '1']
    n = 2
    if level >= 6:
        text += '2. Sell\n'
        options += ['sell', '2']
        n += 1
    text += str(n) + '. Back'
    options += [str(n)]
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == 'buy' or answer == '1':
            text = 'What would you lie to buy?\n\n'
            text += '1. Potions\n'
            text += '2. Materials\n'
            text += '3. Back'
            options = ['1', '2', '3', 'potions', 'potion', 'pot', 'materials', 'material', 'back']
            setTextOutput(text)
            playerButton['text'] = 'Submit'
            await at.event(playerButton, '<Button>')
            answer = grabText()
            if options.__contains__(answer):
                if answer.__contains__('pot') or answer == '1':
                    text = 'Which potion would you like to buy?\n\n'
                    text += '1. Small Health Potion    Heals 10 health points    Cost: 10 coins\n'
                    text += '2. Small MP Potion    Heals 10 MP    Cost: 10 coins\n\n'
                    options = ['1', '2', 'smallhealth', 'smallmp', 'smallhealthpotion', 'smallmppotion']
                    if level >= 4:
                        text += '3. Medium Health Potion    Heals 35 health points    Cost: 55 coins\n'
                        text += '4. Medium MP Potion    Heals 35 MP    Cost: 55 coins\n\n'
                        options += ['3', '4', 'mediumhealth', 'mediummp', 'mediumhealthpotion', 'mediummppotion']
                    if level >= 9:
                        text += '5. Large Health Potion    Heals 75 health points    Cost: 100 coins\n'
                        text += '6. Large MP Potion    Heals 75 MP    Cost: 100 coins\n\n'
                        options += ['5', '6', 'largehealth', 'largemp', 'largehealthpotion', 'largemppotion']
                    if level >= 14:
                        text += '7. Max Health Potion    Heals all health points    Cost: 175 coins\n'
                        text += '8. Max MP Potion    Heals all MP    Cost: 175 coins\n'
                        options += ['7', '8', 'maxhealth', 'maxmp', 'maxhealthpotion', 'maxmppotion']
                    setTextOutput(text)
                    playerButton['text'] = 'Submit'
                    await at.event(playerButton, '<Button>')
                    answer = grabText()
                    if options.__contains__(answer):
                        coins = playerData['money']
                        if answer.__contains__('smallhealth') or answer == '1':
                            if coins >= 10:
                                text = 'You purchased a small health potion.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                playerData['money'] -= 10
                                playerData['inventory']['small_health_potions'] += 1
                                saveData()
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough coins.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if answer.__contains__('smallmp') or answer == '2':
                            if coins >= 10:
                                text = 'You purchased a small MP potion.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                playerData['money'] -= 10
                                playerData['inventory']['small_mp_potions'] += 1
                                saveData()
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough coins.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if answer.__contains__('mediumhealth') or answer == '3':
                            if coins >= 55:
                                text = 'You purchased a medium health potion.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                playerData['money'] -= 55
                                playerData['inventory']['medium_health_potions'] += 1
                                saveData()
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough coins.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if answer.__contains__('mediummp') or answer == '4':
                            if coins >= 55:
                                text = 'You purchased a medium MP potion.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                playerData['money'] -= 55
                                playerData['inventory']['medium_mp_potions'] += 1
                                saveData()
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough coins.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if answer.__contains__('largehealth') or answer == '5':
                            if coins >= 100:
                                text = 'You purchased a large health potion.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                playerData['money'] -= 100
                                playerData['inventory']['large_health_potions'] += 1
                                saveData()
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough coins.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if answer.__contains__('largemp') or answer == '6':
                            if coins >= 100:
                                text = 'You purchased a large MP potion.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                playerData['money'] -= 100
                                playerData['inventory']['large_mp_potions'] += 1
                                saveData()
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough coins.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if answer.__contains__('maxhealth') or answer == '7':
                            if coins >= 175:
                                text = 'You purchased a max health potion.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                playerData['money'] -= 175
                                playerData['inventory']['max_health_potions'] += 1
                                saveData()
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough coins.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if answer.__contains__('maxmp') or answer == '8':
                            if coins >= 175:
                                text = 'You purchased a max MP potion.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                playerData['money'] -= 175
                                playerData['inventory']['max_mp_potions'] += 1
                                saveData()
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough coins.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                    else:
                        text = 'That is not an answer.'
                        setTextOutput(text)
                        playerButton['text'] = 'Next'
                        await at.event(playerButton, '<Button>')
                        at.start(shop())
                if answer == 'materials' or answer == '2':
                    text = 'What materials would you like to buy.\n\n'
                    text += '1. Wood    2 coins\n'
                    text += '2. Stone    3 coins\n'
                    options += ['1', '2', 'wood', 'stone']
                    if level >= 6:
                        text += '3. Iron Ore    10 coins\n'
                        text += '4. Gold Ore    15 coins\n'
                        options += ['3', '4', 'ironore', 'goldore']
                    if level >= 8:
                        text += '5. Iron    20 coins\n'
                        text += '6. Gold    30 coins'
                        options += ['5', '6', 'iron', 'gold']
                    setTextOutput(text)
                    playerButton['text'] = 'Submit'
                    await at.event(playerButton, '<Button>')
                    item = grabText()
                    if options.__contains__(item):
                        coins = playerData['money']
                        text = 'How much would you like to buy?'
                        setTextOutput(text)
                        await at.event(playerButton, '<Button>')
                        answer = grabText()
                        if item == 'wood' or item == '1':
                            money_needed = 2 * int(answer)
                            if money_needed < coins:
                                text = 'You brought ' + answer + ' wood for ' + str(money_needed) + ' coins.'
                                setTextOutput(text)
                                playerData['wood'] += int(answer)
                                playerData['money'] -= money_needed
                                saveData()
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough money.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if item == 'stone' or item == '2':
                            money_needed = 3 * int(answer)
                            if money_needed < coins:
                                text = 'You brought ' + answer + ' stone for ' + str(money_needed) + ' coins.'
                                setTextOutput(text)
                                playerData['stone'] += int(answer)
                                playerData['money'] -= money_needed
                                saveData()
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough money.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if item == 'ironore' or item == '3':
                            money_needed = 10 * int(answer)
                            if money_needed < coins:
                                text = 'You brought ' + answer + ' iron ore for ' + str(money_needed) + ' coins.'
                                setTextOutput(text)
                                playerData['iron_ore'] += int(answer)
                                playerData['money'] -= money_needed
                                saveData()
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough money.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if item == 'goldore' or item == '4':
                            money_needed = 15 * int(answer)
                            if money_needed < coins:
                                text = 'You brought ' + answer + ' gold ore for ' + str(money_needed) + ' coins.'
                                setTextOutput(text)
                                playerData['gold_ore'] += int(answer)
                                playerData['money'] -= money_needed
                                saveData()
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough money.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if item == 'iron' or item == '5':
                            money_needed = 20 * int(answer)
                            if money_needed < coins:
                                text = 'You brought ' + answer + ' iron for ' + str(money_needed) + ' coins.'
                                setTextOutput(text)
                                playerData['iron'] += int(answer)
                                playerData['money'] -= money_needed
                                saveData()
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough money.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                        if item == 'gold' or item == '6':
                            money_needed = 30 * int(answer)
                            if money_needed < coins:
                                text = 'You brought ' + answer + ' gold for ' + str(money_needed) + ' coins.'
                                setTextOutput(text)
                                playerData['gold'] += int(answer)
                                playerData['money'] -= money_needed
                                saveData()
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(gameLoop())
                            else:
                                text = 'You do not have enough money.'
                                setTextOutput(text)
                                playerButton['text'] = 'Next'
                                await at.event(playerButton, '<Button>')
                                at.start(shop())
                    else:
                        text = 'That is not something you can buy.'
                        setTextOutput(text)
                        playerButton['text'] = 'Next'
                        await at.event(playerButton, '<Button>')
                        at.start(shop())
                if answer == 'back' or answer == '3':
                    at.start(gameLoop())
            else:
                text = 'That is not something you can buy.'
                setTextOutput(text)
                playerButton['text'] = 'Next'
                await at.event(playerButton, '<Button>')
                at.start(shop())
        if (answer == 'sell' or answer == '2') and level >= 6:
            text = 'What would you like to sell?\n\n'
            text += '1. Wood: x' + str(playerData['wood']) + '    1 coin.\n'
            text += '2. Stone: x' + str(playerData['stone']) + '    2 coins\n'
            text += '3. Iron Ore: x' + str(playerData['iron_ore']) + '    5 coins\n'
            text += '4. Gold Ore: x' + str(playerData['gold_ore']) + '    8 coins\n'
            text += '5. Iron: x' + str(playerData['iron']) + '    15 coins\n'
            text += '6. Gold: x' + str(playerData['gold']) + '    25 coins\n'
            text += '7. Back'
            setTextOutput(text)
            playerButton['text'] = 'Submit'
            await at.event(playerButton, '<Button>')
            item = grabText()
            options = ['1', '2', '3', '4', '5', '6', '7', 'wood', 'stone', 'ironore', 'goldore', 'iron', 'gold', 'back']
            if options.__contains__(item):
                if item == 'back' or item == '7':
                    at.start(gameLoop())
                else:
                    text = 'How many would you like to sell.'
                    setTextOutput(text)
                    await at.event(playerButton, '<Button>')
                    answer = grabText()
                    num = int(answer)
                    if item == 'wood' or item == '1':
                        if playerData['wood'] >= num:
                            coins_gained = num
                            text = 'You sold ' + str(num) + ' wood for ' + str(coins_gained) + ' coins.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            playerData['wood'] -= num
                            playerData['money'] += coins_gained
                            saveData()
                            at.start(gameLoop())
                        else:
                            text = 'You do not have enough resources for that.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            at.start(shop())
                    if item == 'stone' or item == '2':
                        if playerData['stone'] >= num:
                            coins_gained = num * 2
                            text = 'You sold ' + str(num) + ' stone for ' + str(coins_gained) + ' coins.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            playerData['stone'] -= num
                            playerData['money'] += coins_gained
                            saveData()
                            at.start(gameLoop())
                        else:
                            text = 'You do not have enough resources for that.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            at.start(shop())
                    if item == 'ironore' or item == '3':
                        if playerData['iron_ore'] >= num:
                            coins_gained = num * 5
                            text = 'You sold ' + str(num) + ' iron ore for ' + str(coins_gained) + ' coins.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            playerData['iron_ore'] -= num
                            playerData['money'] += coins_gained
                            saveData()
                            at.start(gameLoop())
                        else:
                            text = 'You do not have enough resources for that.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            at.start(shop())
                    if item == 'goldore' or item == '4':
                        if playerData['gold_ore'] >= num:
                            coins_gained = num * 8
                            text = 'You sold ' + str(num) + ' gold ore for ' + str(coins_gained) + ' coins.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            playerData['gold_ore'] -= num
                            playerData['money'] += coins_gained
                            saveData()
                            at.start(gameLoop())
                        else:
                            text = 'You do not have enough resources for that.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            at.start(shop())
                    if item == 'iron' or item == '5':
                        if playerData['iron'] >= num:
                            coins_gained = num * 15
                            text = 'You sold ' + str(num) + ' iron for ' + str(coins_gained) + ' coins.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            playerData['iron'] -= num
                            playerData['money'] += coins_gained
                            saveData()
                            at.start(gameLoop())
                        else:
                            text = 'You do not have enough resources for that.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            at.start(shop())
                    if item == 'gold' or item == '6':
                        if playerData['gold'] >= num:
                            coins_gained = num * 25
                            text = 'You sold ' + str(num) + ' gold for ' + str(coins_gained) + ' coins.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            playerData['gold'] -= num
                            playerData['money'] += coins_gained
                            saveData()
                            at.start(gameLoop())
                        else:
                            text = 'You do not have enough resources for that.'
                            setTextOutput(text)
                            playerButton['text'] = 'Next'
                            await at.event(playerButton, '<Button>')
                            at.start(shop())
            else:
                text = 'That is not something you can sell.'
                setTextOutput(text)
                playerButton['text'] = 'Next'
                await at.event(playerButton, '<Button>')
                at.start(shop())
        if answer == 'back' or answer == str(n):
            at.start(gameLoop())
    else:
        text = 'That is not an answer.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(shop())


async def smelt():
    # Craft new weapons
    # Craft new armors
    # Smelt iron and gold ore to make bars.
    global playerData

    text = 'Welcome to the blacksmiths.\n'
    text += 'What would you like to smelt?\n\n'
    text += '1. Iron    Requires: 1 iron ore, 1 wood    Cost 10 coins\n'
    text += '2. Gold    Requires: 1 gold ore, 2 wood    Cost 15 coins\n'
    text += '3. Back'
    options = ['1', '2', '3', 'iron', 'gold', 'back']
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    item = grabText()
    if options.__contains__(item):
        if item == 'back' or item == '3':
            at.start(gameLoop())
        else:
            text = 'How much would you like to make?'
            setTextOutput(text)
            await at.event(playerButton, '<Button>')
            answer = grabText()
            if item == 'iron' or item == '1':
                money_needed = 10 * int(answer)
                if playerData['iron_ore'] >= int(answer) and playerData['wood'] >= int(answer) and playerData['money'] >= money_needed:
                    text = 'You made ' + answer + ' iron.'
                    setTextOutput(text)
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    playerData['iron_ore'] -= int(answer)
                    playerData['wood'] -= int(answer)
                    playerData['money'] -= money_needed
                    playerData['iron'] += int(answer)
                    saveData()
                    at.start(gameLoop())
                else:
                    text = 'You do not have enough resources to make that.'
                    setTextOutput(text)
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    at.start(smelt())
            if item == 'gold' or item == '2':
                money_needed = 15 * int(answer)
                if playerData['gold_ore'] >= int(answer) and playerData['wood'] >= (int(answer) * 2) and playerData['money'] >= money_needed:
                    text = 'You made ' + answer + ' gold.'
                    setTextOutput(text)
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    playerData['gold_ore'] -= int(answer)
                    playerData['wood'] -= int(answer) * 2
                    playerData['money'] -= money_needed
                    playerData['gold'] += int(answer)
                    saveData()
                    at.start(gameLoop())
                else:
                    text = 'You do not have enough resources to make that.'
                    setTextOutput(text)
                    playerButton['text'] = 'Next'
                    await at.event(playerButton, '<Button>')
                    at.start(smelt())
    else:
        text = 'That is not something you can make.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(smelt())


async def travel():
    # Sends player to a new world.
    global playerData
    level = playerData['level']

    text = 'Where would you like to go?\n\n'
    text += '1. Green Field\n'
    n = 2
    options = ['greenfield', '1', 'back']
    if level >= 7:
        text += '2. Deep Forest\n'
        options += ['deepforest', '2']
        n += 1
    if level >= 9:
        text += '3. Ice Plain\n'
        options += ['iceplain', '3']
        n += 1
    if level >= 13:
        text += '4. Lava Cave\n'
        options += ['lavacave', '4']
        n += 1
    if level >= 18:
        text += '5.Sky City\n'
        options += ['skycity', '5']
        n += 1
    if level >= 24:
        text += '6. Dark Descent\n'
        options += ['darkdescent', '6']
        n += 1
    text += str(n) + '. Back'
    options += [str(n)]
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == 'back' or answer == str(n):
            at.start(gameLoop())
        else:
            text = 'Travelling to '
            if answer == 'greenfield' or answer == '1':
                text += 'Green Field...'
                playerData['world'] = 'Green Field'
            if answer == 'deepforest' or answer == '2':
                text += 'Deep Forest...'
                playerData['world'] = 'Deep Forest'
            if answer == 'iceplain' or answer == '3':
                text += 'Ice Plain...'
                playerData['world'] = ' Ice Plain'
            if answer == 'lavacave' or answer == '4':
                text += 'Lava Cave...'
                playerData['world'] = 'Lava Cave'
            if answer == 'skycity' or answer == '5':
                text += 'Sky City...'
                playerData['world'] = 'Sky City'
            if answer == 'darkdescent' or answer == '6':
                text += 'Dark Descent...'
                playerData['world'] = 'Dark Descent'
            setTextOutput(text)
            playerButton['text'] = 'Next'
            await at.event(playerButton, '<Button>')
            saveData()
            at.start(gameLoop())
    else:
        text = 'That place does not exist.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(travel())


async def quests():
    # TODO Quests
    # Gives player new quests
    # Player gets rewards for completing quests
    global playerData

    text = 'Welcome to the quest board.'
    setTextOutput(text)


async def dojo():
    # TODO Dojo
    # Allows player to upgrade moves
    global playerData

    text = 'Welcome to the dojo.'
    setTextOutput(text)


async def enchant():
    # TODO Enchant
    # Allows player to enchant weapons and armor to make them stronger
    global playerData

    text = 'What would you like to enchant?'
    setTextOutput(text)


async def checkLevelup():
    global playerData

    exp_needed = math.floor(50 * (playerData['level'] ** 1.2))

    if playerData['exp'] >= exp_needed:
        level = playerData['level'] + 1
        text = 'You level up to level' + str(level) + '\n'
        if level == 3:
            text += 'You have unlocked the shop.\n'
        if level == 4:
            text += 'You can now buy medium potions in the shop.\n'
        if level == 5:
            text += 'You have unlocked the blacksmiths.\n'
        if level == 6:
            text += 'You can now sell things in the shop.\n'
            text += 'You can now buy ore from the shop.\n'
        if level == 7:
            text += 'You can now travel to different places in the world.\n'
            text += 'You can now travel to the deep forest.\n'
        if level == 9:
            text += 'You can now buy large potions at the shop.\n'
            text += 'You can now travel to the ice plain.\n'
        if level == 13:
            text += 'You can now travel to the lava cave.\n'
        if level == 14:
            text += 'You can now buy max potions at the shop.\n'
        if level == 18:
            text += 'You can now travel to the sky city.\n'
        if level == 24:
            text += 'You can now travel to the dark descent.\n'
        # TODO Finish adding level up unlocks.
        text += '\nWould you like to upgrade.\n'
        text += '1. Attack    Increase attack power by 1.\n'
        text += '2. Defense    Increase defense by 1.\n'
        options = ['1', '2', 'attack', 'defense']
        setTextOutput(text)
        playerButton['text'] = 'Submit'
        await at.event(playerButton, '<Button>')
        answer = grabText()
        # TODO Add option to upgrade damage or defense.
        if options.__contains__(answer):
            playerData['level'] += 1
            if answer == '1' or answer == 'attack':
                text = 'You got +1 attack.\n'
                text += 'All your attacks will now deal one extra damage.'
            if answer == '2' or answer == 'defense':
                text = 'You got +1 defense.\n'
                text += 'You will now take one less damage from attacks.'
        else:
            text = 'That is not an answer.'
            setTextOutput(text)
            playerButton['text'] = 'Next'
            await at.event(playerButton, '<Button>')
            at.start(checkLevelup())


def setTextOutput(text):
    t1 = Thread(target=renderText, args=(text,))
    t1.run()


def renderText(text):
    global settingsData
    textOutput.configure(state='normal')
    if settingsData['textSpeed'] == 0:
        textOutput.delete(0.0, END)
        textOutput.insert(END, text)
    else:
        word = list(text)
        textOutput.delete(0.0, END)
        for char in word:
            textOutput.insert(END, char)
            textOutput.update()
            time.sleep(settingsData['textSpeed'])
    textOutput.configure(state='disabled')
    return


def updatePlayerStats():
    t2 = Thread(target=renderPlayerStats)
    t2.run()


def renderPlayerStats():
    global playerData
    playerStatsOutput.configure(state='normal')
    playerEquipOutput.configure(state='normal')

    playerStatsOutput.delete(0.0, END)
    playerEquipOutput.delete(0.0, END)

    exp_needed = math.floor(50 * (playerData['level'] ** 1.2))

    statsText = 'Name: ' + playerData['name'] + '\n'
    statsText += 'Level: ' + str(playerData['level']) + '\n'
    statsText += 'Exp: ' + str(playerData['exp']) + ' /  ' + str(exp_needed) + '\n'
    statsText += 'Health: ' + str(playerData['health']) + ' / ' + str(playerData['health_max']) + '\n'
    statsText += 'MP: ' + str(playerData['mp']) + ' / ' + str(playerData['mp_max']) + '\n'
    statsText += 'Wood: ' + str(playerData['wood']) + '\n'
    statsText += 'Stone: ' + str(playerData['stone']) + '\n'
    statsText += 'Iron Ore: ' + str(playerData['iron_ore']) + ' / Iron: ' + str(playerData['iron']) + '\n'
    statsText += 'Gold Ore: ' + str(playerData['gold_ore']) + ' / Gold: ' + str(playerData['gold']) + '\n'
    statsText += 'Coins: ' + str(playerData['money'])

    equipText = 'Class: ' + playerData['type_class'].capitalize()
    equipText += '\nWeapon: ' + playerData['weapon'].capitalize()
    equipText += '\nArmor: ' + playerData['armor'].capitalize()
    equipText += '\nWorld: ' + playerData['world']
    equipText += '\nCurrent Quest: ' + playerData['current_quest']

    playerStatsOutput.insert(END, statsText)
    playerEquipOutput.insert(END, equipText)

    playerStatsOutput.configure(state='disabled')
    playerEquipOutput.configure(state='disabled')


def grabText():
    answer = playerAnswerBox.get().replace(' ', '').lower()
    playerAnswerBox.delete(0, END)
    return answer


def saveData():
    global playerData
    global slotNumber
    global settingsData
    global battleData

    if slotNumber == 1:
        with open('playerData/saveOneData.json', 'w') as outfile:
            saveJson = json.dumps(playerData)
            json.dump(saveJson, outfile)
    if slotNumber == 2:
        with open('playerData/saveTwoData.json', 'w') as outfile:
            saveJson = json.dumps(playerData)
            json.dump(saveJson, outfile)
    if slotNumber == 3:
        with open('playerData/saveThreeData.json', 'w') as outfile:
            saveJson = json.dumps(playerData)
            json.dump(saveJson, outfile)

    with open('gameData/settings.json', 'w') as outfile:
        saveJson = json.dumps(settingsData)
        json.dump(saveJson, outfile)
    with open('gameData/battleData.json', 'w') as outfile:
        saveJson = json.dumps(battleData)
        json.dump(saveJson, outfile)


def loadData():
    global settingsData
    global battleData
    global enemyData
    global attackData
    global saveOne
    global saveTwo
    global saveThree

    with open('gameData/settings.json') as json_file:
        data = json.load(json_file)
        settingsData = json.loads(data)

    with open('gameData/battleData.json') as json_file:
        data = json.load(json_file)
        battleData = json.loads(data)

    with open('gameData/enemyData.json') as json_file:
        data = json.load(json_file)
        enemyData = json.loads(data)

    with open('gameData/attackData.json') as json_file:
        data = json.load(json_file)
        attackData = json.loads(data)

    with open('playerData/saveOneData.json') as json_file:
        data = json.load(json_file)
        saveOne = json.loads(data)

    with open('playerData/saveTwoData.json') as json_file:
        data = json.load(json_file)
        saveTwo = json.loads(data)

    with open('playerData/saveThreeData.json') as json_file:
        data = json.load(json_file)
        saveThree = json.loads(data)


def erasePlayerData(slot):
    saveOverride = {'name': 'Empty', 'type_class': 'none', 'level': 0, 'exp': 0}
    saveOverrideJson = json.dumps(saveOverride)

    if slot == '1':
        with open('playerData/saveOneData.json', 'w') as outfile:
            json.dump(saveOverrideJson, outfile)
    if slot == '2':
        with open('playerData/saveTwoData.json', 'w') as outfile:
            json.dump(saveOverrideJson, outfile)
    if slot == '3':
        with open('playerData/saveThreeData.json', 'w') as outfile:
            json.dump(saveOverrideJson, outfile)


def exitGame():
    saveData()
    window.destroy()
    exit()


# Setup game buttons
playerButton = Button(window, text='Next', width='7', bg='gray', fg='white', font='times 16')
playerButton.grid(row=4, column=0, sticky='w')
exitButton = Button(window, text='Exit', width='7', command=exitGame, bg='gray', fg='white', font='times 16')
exitButton.grid(row=5, column=0, sticky='w')

at.start(startGame())

window.mainloop()
