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
    text = 'Welcome to Xenorule!\n'
    text += 'What would you like to do?\n\n'
    text += 'Play\n'
    options = ['play']
    text += 'Erase\n'
    options.append('erase')
    text += 'Settings\n'
    options.append('settings')
    text += 'Exit'
    options.append('exit')
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == 'play':
            at.start(playerSelect())
        if answer == 'settings':
            at.start(settings())
    else:
        text = 'That is not an options.'
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
    options = ['1', '2', '3,']
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if options.__contains__(answer):
        if answer == '1':
            var = not pd.settings['backgroundMusic']
            pd.settings['backgroundMusic'] = var
            saveData()
            at.start(settings())
        if answer == '2':
            var = not pd.settings['soundFX']
            pd.settings['soundFX'] = var
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


async def playerSelect():
    global playerData
    global slotNumber
    text = 'What save would you like to use?\n'
    text += 'Save One: ' + pd.saveOne['name'] + '\n'
    text += 'Save Two: ' + pd.saveTwo['name'] + '\n'
    text += 'Save Three: ' + pd.saveThree['name'] + '\n'
    text += 'Answer: One, Two, Three'
    setTextOutput(text)
    playerButton['text'] = 'Submit'
    await at.event(playerButton, '<Button>')
    answer = grabText()
    if answer == 'one':
        playerData = pd.saveOne
        slotNumber = 1
        if playerData['name'] == 'Empty':
            at.start(newGame())
        else:
            at.start(gameLoop())
    elif answer == 'two':
        playerData = pd.saveTwo
        slotNumber = 2
        if playerData['name'] == 'Empty':
            at.start(newGame())
        else:
            at.start(gameLoop())
    elif answer == 'three':
        playerData = pd.saveThree
        slotNumber = 3
        if playerData['name'] == 'Empty':
            at.start(newGame())
        else:
            at.start(gameLoop())
    else:
        text = 'That is not an answer.'
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
    answer = playerAnswerBox.get().capitalize()
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
    text = 'Welcome ' + answer + ', are for your adventure to begin.'
    saveData()
    setTextOutput(text)
    playerButton['text'] = 'Next'
    await at.event(playerButton, '<Button>')
    at.start(gameLoop())


async def gameLoop():
    global playerData

    # Update PlayerStats and equipment text
    updatePlayerStats()

    text = 'What would you like to do?'
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

    statsText = 'Name: ' + playerData['name'] + '\n'
    statsText += 'Level: ' + str(playerData['level']) + '\n'
    statsText += 'Exp: ' + str(playerData['exp']) + '\n'
    statsText += 'Health: ' + str(playerData['health']) + ' / ' + str(playerData['health_max']) + '\n'
    statsText += 'MP: ' + str(playerData['mp']) + ' / ' + str(playerData['mp_max']) + '\n'
    statsText += 'Wood: ' + str(playerData['wood']) + '\n'
    statsText += 'Stone: ' + str(playerData['stone']) + '\n'
    statsText += 'Iron ore: ' + str(playerData['iron_ore']) + ' / Iron: ' + str(playerData['iron']) + '\n'
    statsText += 'Gold ore: ' + str(playerData['gold_ore']) + ' / Gold: ' + str(playerData['gold']) + '\n'
    statsText += 'Coins: ' + str(playerData['money'])

    equipText = ''

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
# nextButton = Button(window, text='Next', width='6', bg='gray', fg='white', font='times 16')
# nextButton.grid(row=4, column=0, sticky='w')
# submitButton = Button(window, text='Submit', width='6', bg='gray', fg='white', font='times 16')
# submitButton.grid(row=5, column=0, sticky='w')
playerButton = Button(window, text='Next', width='6', bg='gray', fg='white', font='times 16')
playerButton.grid(row=4, column=0, sticky='w')
exitButton = Button(window, text='Exit', width='6', command=exitGame, bg='gray', fg='white', font='times 16')
exitButton.grid(row=5, column=0, sticky='w')

at.start(startGame())

window.mainloop()
