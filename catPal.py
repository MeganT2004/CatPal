#CatPal Project

from tkinter import *
from PIL import Image, ImageTk, ImageFilter
import time
import os, glob
import ctypes
from ctypes import wintypes

#getting usable area (window excluding taskbar)
def get_work_area():
    SPI_GETWORKAREA = 0x0030
    rect = wintypes.RECT()
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_GETWORKAREA,
        0,
        ctypes.byref(rect),
        0
    )
    return rect.left, rect.top, rect.right, rect.bottom

left, top, right, bottom = get_work_area()
screen_w = right - left
screen_h = bottom - top

#Transparency setup
TRANSPARENT_COLOR = "#ff00ff"
CUTOUT_THRESHOLD = 60
GROW = 1

def imageLoad(PATH): #Image load/clean up edges/remove halo
    pil = Image.open(PATH).convert("RGBA")
    w, h = pil.size

    r, g, b, a = pil.split()
    mask = a.point(lambda px: 255 if px >= CUTOUT_THRESHOLD else 0)

    if GROW > 1:
        mask = mask.filter(ImageFilter.MaxFilter(GROW))

    bg = Image.new("RGB", (w, h), TRANSPARENT_COLOR)
    fg = pil.convert("RGB")
    bg.paste(fg, (0, 0), mask)

    return bg, w, h

window = Tk() #configure window
window.overrideredirect(True)
window.attributes("-topmost", True)
window.configure(bg=TRANSPARENT_COLOR)

bgBase, wb, hb = imageLoad("cat2test.png")

imgBase = ImageTk.PhotoImage(bgBase)

label = Label(window, image=imgBase, bd=0, bg=TRANSPARENT_COLOR, highlightthickness=0)
label.pack()

window.update_idletasks()
try:
    window.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
except TclError:
    pass

x = right - wb
y = bottom - hb

window.geometry(f"{wb}x{hb}+{x-300}+{y}")

window.mainloop()
