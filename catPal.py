#CatPal Project

from tkinter import *
from PIL import Image, ImageTk, ImageFilter
import time
import os, glob

window = Tk()
window.config(highlightbackground='#000000')
canvas = Canvas(window, width=500, height=500, background='#000000', bd=0)
canvas.pack()
label = Label(canvas,borderwidth=0,bg='#000000')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','#000000')
window.wm_attributes('-topmost', True)
canvas.create_window(0, 0, anchor=NW, window=label)
img = PhotoImage(file='testPNG.png')
canvas.create_image(250, 250, image=img)
mainloop()
