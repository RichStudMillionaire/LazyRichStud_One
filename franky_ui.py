from credit_cards_ui import CreditCards

import tkinter as tk
from tkinter import ttk

#cc = CreditCards()

from tkinter import *
import tkinter as tk

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Create an instance of tkinter frame
win = Tk()

# Set the dimensions of the window
width = 600
height = 250

# Center the window
center_window(win, width, height)

cc= CreditCards(win,0,0)

win.mainloop()