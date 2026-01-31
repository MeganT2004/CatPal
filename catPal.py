#CatPal Project

from tkinter import *
from PIL import Image, ImageTk, ImageFilter
import time
import os
import ctypes
from ctypes import wintypes
from pynput import mouse

cat_busy = False

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
bgLClick, wc, hc = imageLoad("cat2love.png")
bgRClick, wd, hd = imageLoad("cat2down.png")
bgSleep, wd, hd = imageLoad("cat2sleep.png")

img_base = ImageTk.PhotoImage(bgBase)
img_l_click = ImageTk.PhotoImage(bgLClick)
img_r_click = ImageTk.PhotoImage(bgRClick)
img_sleep = ImageTk.PhotoImage(bgSleep)

label = Label(window, image=img_base, bd=0, bg=TRANSPARENT_COLOR, highlightthickness=0)
label.pack()

#catLove Event (LClick, timer)
def on_cat_click(event):
    global cat_busy
    cat_busy = True
    label.config(image=img_l_click)
    label.image = img_l_click

    #after 2 seconds, restore
    window.after(2000, restore_cat)

def restore_cat():
    global cat_busy
    label.config(image=img_base)
    label.image = img_base
    cat_busy = False

#CatDown event (RClick)
def cat_down_click(event):
    global cat_busy
    cat_busy = True
    label.config(image=img_r_click)
    label.image = img_r_click

    #after 2 seconds, restore
    label.bind("<Button-3>", restore_cat_click)

def restore_cat_click(event):
    global cat_busy
    label.config(image=img_base)
    label.image = img_base
    label.bind("<Button-3>", cat_down_click)
    cat_busy = False

label.bind("<Button-1>", on_cat_click)
label.bind("<Button-3>", cat_down_click)

#Cat Sleep timer (Mouse Idle)
last_move_time = time.time()
mouse_pos = None

def on_move(x, y):
    global last_move_time, mouse_pos
    mouse_pos = (x, y)
    last_move_time = time.time()

listener = mouse.Listener(on_move=on_move)
listener.start()

IDLE_TIME = 30

def go_to_sleep():
    label.config(image=img_sleep)
    label.image = img_sleep

def check_idle():
    current_time = time.time()
    if not cat_busy:
        if current_time - last_move_time > IDLE_TIME:
            go_to_sleep()
        else:
            restore_cat()
    window.after(500, check_idle)  # check every half second

window.update_idletasks()
try:
    window.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
except TclError:
    pass

x = right - wb
y = bottom - hb

window.geometry(f"{wb}x{hb}+{x-300}+{y}")
check_idle()
window.mainloop()
