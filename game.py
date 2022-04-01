from tkinter import *
from PIL import Image, ImageTk
import player_data as pd
import asynctkinter as at

# Setup game window
window = Tk()
window.title('Xenorule')
window.configure(background='black')
window.geometry('1280x720')
window.resizable(width=NO, height=NO)
ico = Image.open('appicon.gif')
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

# Setup text box
playerStatsOutput = Text(window, width=60, height=9, bg='black', fg='white', font='times 16')
playerStatsOutput.grid(row=0, column=0, sticky='w')
playerStatsOutput.configure(state='disabled')
playerEquipOutput = Text(window, width=60, height=9, bg='black', fg='white', font='times 16')
playerEquipOutput.grid(row=0, column=1, sticky='w')
playerEquipOutput.configure(state='disabled')
textOutput = Text(window, width=120, height=14, bg='black', fg='white', font='times 16')
textOutput.grid(row=1, column=0, columnspan=2, sticky='w')
textOutput.configure(state='disabled')
Label(window, text='Answer:', bg='black', fg='white', font='times 16').grid(row=2, column=0, sticky='w')
playerAnswerBox = Entry(window, width=120, bg='black', fg='white', font='times 16')
playerAnswerBox.grid(row=3, column=0, columnspan=2, sticky='w')

slotNumber = 0
playerData = {}


async def startGame():
    global playerData
    global slotNumber
    text = 'What save would you like to use?\n'
    text += 'Save One: ' + pd.saveOne['name'] + '\n'
    text += 'Save Two: ' + pd.saveTwo['name'] + '\n'
    text += 'Save Three: ' + pd.saveThree['name'] + '\n'
    text += 'Answer: One, Two, Three'
    setTextOutput(text)
    await at.event(submitButton, '<Button>')
    answer = grabText()
    if answer == 'one':
        playerData = pd.saveOne
        slotNumber = 1
        if playerData['name'] == 'Empty':
            at.start(newGame(answer))
    if answer == 'two':
        playerData = pd.saveTwo
        slotNumber = 2
        if playerData['name'] == 'Empty':
            at.start(newGame(answer))
    if answer == 'three':
        playerData = pd.saveThree
        slotNumber = 3
        if playerData['name'] == 'Empty':
            at.start(newGame(answer))

# async def gameLoop():
    

async def newGame(number):
    global playerData
    global slotNumber
    text = 'Welcome to Xenorule!\n'
    text += 'What is your name, traveller?'
    setTextOutput(text)
    await at.event(submitButton, '<Button>')
    answer = playerAnswerBox.get().capitalize()
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


def setTextOutput(text):
    textOutput.configure(state='normal')
    textOutput.delete(0.0, END)
    textOutput.insert(END, text)
    textOutput.configure(state='disabled')


def updatePlayerStats():
    playerStatsOutput.configure(state='normal')
    playerEquipOutput.configure(state='normal')

    playerStatsOutput.delete(0.0, END)
    playerEquipOutput.delete(0.0, END)

    text = ''

    playerStatsOutput.insert(END, text)
    playerEquipOutput.insert(END, text)

    playerStatsOutput.configure(state='disabled')
    playerEquipOutput.configure(state='disabled')


def grabText():
    answer = playerAnswerBox.get().replace(' ', '').lower()
    playerAnswerBox.delete(0, END)
    return answer


def saveData():
    global playerData
    global slotNumber
    f = open('player_data.py', 'w')
    if slotNumber == 1:
        f.write('saveOne = ' + str(playerData) + '\n')
        f.write('saveTwo = ' + str(pd.saveTwo) + '\n')
        f.write('saveThree = ' + str(pd.saveThree) + '\n')
    if slotNumber == 2:
        f.write('saveOne = ' + str(pd.saveOne) + '\n')
        f.write('saveTwo = ' + str(playerData) + '\n')
        f.write('saveThree = ' + str(pd.saveThree) + '\n')
    if slotNumber == 3:
        f.write('saveOne = ' + str(pd.saveOne) + '\n')
        f.write('saveTwo = ' + str(pd.saveTwo) + '\n')
        f.write('saveThree = ' + str(playerData) + '\n')
    f.close()


def exitGame():
    window.destroy()
    exit()


# Setup game buttons
nextButton = Button(window, text='Next', width='6', bg='gray', fg='white', font='times 16')
nextButton.grid(row=4, column=0, sticky='w')
submitButton = Button(window, text='Submit', width='6', bg='gray', fg='white', font='times 16')
submitButton.grid(row=5, column=0, sticky='w')
exitButton = Button(window, text='Exit', width='6', command=exitGame, bg='gray', fg='white', font='times 16')
exitButton.grid(row=6, column=0, sticky='w')


at.start(startGame())

window.mainloop()
