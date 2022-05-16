import asyncio
import time
from tkinter import *
from PIL import Image, ImageTk


window = Tk()
window.title('Xenorule')
window.configure(background='black')
window.geometry('1280x720')
window.resizable(width=NO, height=NO)
window.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('appicon.gif')))
fullscreen = False
window.attributes('-fullscreen', fullscreen)
# window.state('zoomed')



def resizeSmallWindow():
    window.geometry('128x72')


def resizeBigWindow():
    window.geometry('1280x720')


def destroyButton():
    Button1.destroy()
    Button4 = Button(window, text='Next', command=destroyButton, width='6', bg='gray', fg='white', font='times 16')
    Button4.grid(row=1, column=0, sticky='w')


def toggleFullscreen():
    global fullscreen
    fullscreen = not fullscreen
    window.attributes('-fullscreen', fullscreen)


def scrollingText():
    text = 'You can now travel to different places in the world.\n'
    text += 'You can now travel to the deep forest.'
    word = list(text)
    textOutput.configure(state='normal')
    textOutput.delete(0.0, END)
    for char in word:
        textOutput.insert(END, char)
        textOutput.update()
        time.sleep(0.01)
        # Instant = 0
        # Fast = 0.01
        # Medium = 0.05
        # Slow = 0.1
    textOutput.configure(state='disabled')



def setTextOutput(text):
    print('setting text')
    textOutput.configure(state='normal')
    textOutput.delete(0.0, END)
    textOutput.insert(END, text)
    textOutput.configure(state='disabled')


def exitGame():
    window.destroy()
    exit()


Button1 = Button(window, text='Next', command=scrollingText, width='6', bg='gray', fg='white', font='times 16')
Button1.grid(row=0, column=0, sticky='w')

Button2 = Button(window, text='Big', command=toggleFullscreen, width='6', bg='gray', fg='white', font='times 16')
Button2.grid(row=1, column=0, sticky='w')

Button3 = Button(window, text='Exit', command=exitGame, width='6', bg='gray', fg='white', font='times 16')
Button3.grid(row=2, column=0, sticky='w')

textOutput = Text(window, width=120, height=13, bg='black', fg='white', font='times 16')
textOutput.grid(row=3, column=0, columnspan=2, sticky='w')



window.mainloop()