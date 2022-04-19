import math
import random
from tkinter import *
from PIL import Image, ImageTk
from saveData import player_data as pd
import asynctkinter as at
import vlc

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


async def startGame():
    bgMusic = vlc.MediaPlayer('sounds/Daredevil.mp3')
    if pd.settings['backgroundMusic']:
        bgMusic.play()
    else:
        bgMusic.stop()
    text = 'Welcome to Xenorule!\n'
    text += 'What would you like to do?\n\n'
    text += '1. Play\n'
    text += '2. Erase\n'
    text += '3. Settings\n'
    text += '4. Exit\n'
    text += 'Answer: 1, 2, 3, 4'
    options = ['play', 'erase', 'settings', 'exit', '1', '2', '3', '4']
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == 'play' or answer == '1':
            at.start(playerSelect())
        if answer == 'erase' or answer == '2':
            print('Erase')
            at.start(erasePlayer())
        if answer == 'settings' or answer == '3':
            at.start(settings())
    else:
        text = 'That is not an options.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(startGame())


async def newGame():
    global playerData
    global slotNumber
    text = 'Welcome to Xenorule!\n'
    text += 'What is your name, traveller?'
    setTextOutput(text)
    playerButton['text'] = 'Submit'
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
    text = 'Welcome ' + answer + ', are you ready for your adventure to begin.'
    saveData()
    setTextOutput(text)
    playerButton['text'] = 'Next'
    await at.event(playerButton, '<Button>')
    at.start(playerSelect())


async def playerSelect():
    global playerData
    global slotNumber
    text = 'What save would you like to use?\n'
    text += '1. ' + pd.saveOne['name'] + '\n'
    text += '2. ' + pd.saveTwo['name'] + '\n'
    text += '3. ' + pd.saveThree['name'] + '\n'
    text += 'Answer: 1, 2, 3'
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if answer == 'one' or answer == '1':
        playerData = pd.saveOne
        slotNumber = 1
        if playerData['name'] == 'Empty':
            at.start(newGame())
        else:
            if playerData['type_class'] == 'none':
                at.start(chooseClass())
            else:
                at.start(gameLoop())
    elif answer == 'two' or answer == '2':
        playerData = pd.saveTwo
        slotNumber = 2
        if playerData['name'] == 'Empty':
            at.start(newGame())
        else:
            if playerData['type_class'] == 'none':
                at.start(chooseClass())
            else:
                at.start(gameLoop())
    elif answer == 'three' or answer == '3':
        playerData = pd.saveThree
        slotNumber = 3
        if playerData['name'] == 'Empty':
            at.start(newGame())
        else:
            if playerData['type_class'] == 'none':
                at.start(chooseClass())
            else:
                at.start(gameLoop())
    else:
        text = 'That is not an answer.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(startGame())


async def settings():
    print('Settings')
    text = 'Settings\n'
    text += '1. Background Music: ' + str(pd.settings['backgroundMusic']) + '\n'
    text += '2. Sound FX: ' + str(pd.settings['soundFX']) + '\n'
    text += '3. Back\n'
    text += 'What settings would you like to change. (1, 2, 3)'
    setTextOutput(text)
    options = ['1', '2', '3']
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == '1':
            pd.settings['backgroundMusic'] = not pd.settings['backgroundMusic']
            saveData()
            at.start(settings())
        if answer == '2':
            pd.settings['soundFX'] = not pd.settings['soundFX']
            saveData()
            at.start(settings())
        if answer == '3':
            at.start(startGame())
    else:
        text = 'That is not an options.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(settings())


async def chooseClass():
    global playerData

    text = 'What class would you like to be?\n'
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
        if answer == 'paladin' or answer == '2':
            text = 'You have selected paladin class.\n'
            text += 'You received a sword.'
            setTextOutput(text)
            playerData['type_class'] = 'paladin'
            playerData['weapon'] = 'sword'
            playerData['weapon_inventory'].append(playerData['weapon'])
        if answer == 'archer' or answer == '3':
            text = 'You are now an archer.\n'
            text += 'You got a bow.'
            setTextOutput(text)
            playerData['type_class'] = 'archer'
            playerData['weapon'] = 'bow'
            playerData['weapon_inventory'].append(playerData['weapon'])
        await at.event(playerButton, '<Button>')
        saveData()
        at.start(playerSelect())
    else:
        text = 'That is not an answer.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(chooseClass())


async def erasePlayer():
    if pd.saveOne['name'] == 'Empty' and pd.saveTwo['name'] == 'Empty' and pd.saveThree['name'] == 'Empty':
        text = 'You do not have any slots to erase.'
        setTextOutput(text)
        playerButton['text'] = 'Next'
        await at.event(playerButton, '<Button>')
        at.start(startGame())
    else:
        text = 'Which slot would you like to erase?\n'
        options = ['exit']
        if pd.saveOne['name'] != 'Empty':
            text += '1. ' + pd.saveOne['name'] + '\n'
            options += ['1']
        if pd.saveTwo['name'] != 'Empty':
            text += '2. ' + pd.saveTwo['name'] + '\n'
            options += ['2']
        if pd.saveThree['name'] != 'Empty':
            text += '3. ' + pd.saveThree['name'] + '\n'
            options += ['3']
        text += 'Options: 1, 2, 3, exit'
        setTextOutput(text)
        playerButton['text'] = 'Submit'
        await at.event(playerButton, '<Button>')
        answer = grabText()
        if options.__contains__(answer):
            if answer == 'exit':
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
                        if eraseSlot == '1':
                            pd.saveOne['name'] = 'Empty'
                            pd.saveOne['type_class'] = 'none'
                        if eraseSlot == '2':
                            pd.saveTwo['name'] = 'Empty'
                            pd.saveTwo['type_class'] = 'none'
                        if eraseSlot == '2':
                            pd.saveThree['name'] = 'Empty'
                            pd.saveThree['type_class'] = 'none'
                        saveData()
                        text = 'Save slot erased.'
                        setTextOutput(text)
                        playerButton['text'] = 'Next'
                        await at.event(playerButton, '<Button>')
                        at.start(startGame())
                    if answer == 'no':
                        at.start(startGame())
        else:
            text = 'That is not an options.'
            setTextOutput(text)
            playerButton['text'] = 'Next'
            await at.event(playerButton, '<Button>')
            at.start(erasePlayer())


async def gameLoop():
    global playerData

    # Update PlayerStats and equipment text
    updatePlayerStats()
    level = playerData['level']
    text = 'What would you like to do?\n'
    text += '1. Chop\n'
    text += '2. Mine\n'
    text += '3. Fight\n'
    text += '4. Heal\n'
    options = ['1', 'chop', '2', 'mine', '3', 'fight', '4', 'heal']
    if level >= 3:
        text += '5. Shop\n'
        options += ['shop', '5']
    if level >= 5:
        text += '6. Smelt\n'
        options += ['smelt', '6']
    if level >= 7:
        text += '7. Travel\n'
        options += ['travel', '7']
    if level >= 10:
        text += '8. Quests\n'
        options += ['quests', '8']
    if level >= 12:
        text += '9. Dojo\n'
        options += ['dojo', '9']
    if level >= 15:
        text += '10. Enchant\n'
        options += ['enchant', '10']

    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
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
                if answer == 'exit' or answer == 'back':
                    at.start(gameLoop())
            else:
                text = 'You do not have that potion.'
                setTextOutput(text)
                playerButton['text'] = 'Next'
                await at.event(playerButton, '<Button>')
                at.start(heal())


async def fight():
    global playerData

    text = 'You start to fight an enemy.'
    setTextOutput(text)


async def shop():
    # Buy health and MP potions
    # Sell Wood, Stone, Iron, Gold for Coins
    global playerData
    level = playerData['level']
    text = 'Welcome to the shop!\n'
    text += 'What would you like to do?\n\n'
    text += '1. Buy\n'
    options = ['back', 'exit', 'buy', '1']
    if level >= 5:
        text += '2. Sell\n'
        options += ['sell', '2']
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == 'buy' or answer == '1':
            text = 'What would you lie to buy?\n\n'
            text += '1. Potions\n'
            text += '2. Materials'
            options = ['1', '2', 'potions', 'potion', 'pot', 'materials', 'material']
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
                    if level >= 13:
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
                    if level >= 5:
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
            else:
                text = 'That is not something you can buy.'
                setTextOutput(text)
                playerButton['text'] = 'Next'
                await at.event(playerButton, '<Button>')
                at.start(shop())
        if answer == 'sell' or answer == '2':
            text = 'What would you like to sell?\n\n'
            text += '1. Wood: x' + str(playerData['wood']) + '    1 coin.\n'
            text += '2. Stone: x' + str(playerData['stone']) + '    2 coins\n'
            text += '3. Iron Ore: x' + str(playerData['iron_ore']) + '    5 coins\n'
            text += '4. Gold Ore: x' + str(playerData['gold_ore']) + '    8 coins\n'
            text += '5. Iron: x' + str(playerData['iron']) + '    15 coins\n'
            text += '6. Gold: x' + str(playerData['gold']) + '    25 coins\n'
            setTextOutput(text)
            playerButton['text'] = 'Submit'
            await at.event(playerButton, '<Button>')
            item = grabText()
            options = ['1', '2', '3', '4', '5', '6', 'wood', 'stone', 'ironore', 'goldore', 'iron', 'gold']
            if options.__contains__(item):
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
    text += '1. Iron    Requires: 1 iron ore, 1 wood\n'
    text += '2. Gold    Requires: 1 gold ore, 2 wood\n'
    options = ['1', '2', 'iron', 'gold']
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    item = grabText()
    if options.__contains__(item):
        text = 'How much would you like to make?'
    setTextOutput(text)


async def travel():
    # Sends player to a new world.
    global playerData

    text = 'Where would you like to go?'
    setTextOutput(text)


async def quests():
    # Gives player new quests
    # PLayer gets rewards for completing quests
    global playerData

    text = 'Welcome to the quest board.'
    setTextOutput(text)


async def dojo():
    # Allows player to upgrade moves
    global playerData

    text = 'Welcome to the dojo.'
    setTextOutput(text)


async def enchant():
    # Allows player to enchant weapons and armor to make them stronger
    global playerData

    text = 'What would you like to enchant?'
    setTextOutput(text)


def setTextOutput(text):
    textOutput.configure(state='normal')
    textOutput.delete(0.0, END)
    textOutput.insert(END, text)
    textOutput.configure(state='disabled')


def updatePlayerStats():
    global playerData
    playerStatsOutput.configure(state='normal')
    playerEquipOutput.configure(state='normal')

    playerStatsOutput.delete(0.0, END)
    playerEquipOutput.delete(0.0, END)

    exp_needed = math.floor(50*(playerData['level'] ** 1.2))

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
    equipText += '\nWorld: ' + playerData['world'].capitalize()
    equipText += '\nCurrent Quest: ' + playerData['current_quest'].capitalize()

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
    f = open('saveData/player_data.py', 'w')
    if slotNumber == 0:
        f.write('saveOne = ' + str(pd.saveOne) + '\n')
        f.write('saveTwo = ' + str(pd.saveTwo) + '\n')
        f.write('saveThree = ' + str(pd.saveThree) + '\n')
        f.write('settings = ' + str(pd.settings))
    if slotNumber == 1:
        f.write('saveOne = ' + str(playerData) + '\n')
        f.write('saveTwo = ' + str(pd.saveTwo) + '\n')
        f.write('saveThree = ' + str(pd.saveThree) + '\n')
        f.write('settings = ' + str(pd.settings))
    if slotNumber == 2:
        f.write('saveOne = ' + str(pd.saveOne) + '\n')
        f.write('saveTwo = ' + str(playerData) + '\n')
        f.write('saveThree = ' + str(pd.saveThree) + '\n')
        f.write('settings = ' + str(pd.settings))
    if slotNumber == 3:
        f.write('saveOne = ' + str(pd.saveOne) + '\n')
        f.write('saveTwo = ' + str(pd.saveTwo) + '\n')
        f.write('saveThree = ' + str(playerData) + '\n')
        f.write('settings = ' + str(pd.settings))
    f.close()


def exitGame():
    saveData()
    window.destroy()
    exit()


# Setup game buttons
playerButton = Button(window, text='Next', width='6', bg='gray', fg='white', font='times 16')
playerButton.grid(row=4, column=0, sticky='w')
exitButton = Button(window, text='Exit', width='6', command=exitGame, bg='gray', fg='white', font='times 16')
exitButton.grid(row=5, column=0, sticky='w')

at.start(startGame())

window.mainloop()
