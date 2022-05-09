from tkinter import *
from PIL import Image, ImageTk
import asynctkinter as at

window = Tk()
window.title('Xenorule')
window.configure(background='black')
window.geometry('1280x720')
window.resizable(width=NO, height=NO)
window.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('appicon.ico')))
window.attributes('-fullscreen', True)
# window.state('zoomed')
fullscreen = True


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


def exitGame():
    window.destroy()
    exit()


Button1 = Button(window, text='Next', command=destroyButton, width='6', bg='gray', fg='white', font='times 16')
Button1.grid(row=0, column=0, sticky='w')

Button2 = Button(window, text='Big', command=toggleFullscreen, width='6', bg='gray', fg='white', font='times 16')
Button2.grid(row=1, column=0, sticky='w')

Button3 = Button(window, text='Exit', command=exitGame, width='6', bg='gray', fg='white', font='times 16')
Button3.grid(row=2, column=0, sticky='w')


window.mainloop()