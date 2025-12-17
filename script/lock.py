#!/usr/bin/env python3
import tkinter as tk
import subprocess
import os


TEXT = (
    "Je viens après P,\n"
    "je ne marche jamais sans U,\n"
    "presse-moi pour sortir."
)

TERMLOCK = "/sgoinfre/goinfre/Perso/zcadinot/script/fc/ft_connect/script/termlock.py"
TERMUNLOCK = "/sgoinfre/goinfre/Perso/zcadinot/script/fc/ft_connect/script/termunlock.py"


def lock_terminal():
    if os.path.exists(TERMLOCK):
        subprocess.Popen(["python3", TERMLOCK],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)


def unlock_terminal():
    if os.path.exists(TERMUNLOCK):
        subprocess.Popen(["python3", TERMUNLOCK],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)


def on_key(event):
    if event.keysym.lower() == "q":
        unlock_terminal()
        root.destroy()
    return "break"


def block_event(event):
    return "break"


def rgb_loop():
    global r, g, b, dr, dg, db

    r += dr
    g += dg
    b += db

    if r <= 0 or r >= 255:
        dr *= -1
    if g <= 0 or g >= 255:
        dg *= -1
    if b <= 0 or b >= 255:
        db *= -1

    color = f"#{r:02x}{g:02x}{b:02x}"
    root.configure(bg=color)
    label.configure(bg=color)

    root.after(20, rgb_loop)


root = tk.Tk()

root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.protocol("WM_DELETE_WINDOW", lambda: None)

root.bind("<Alt-F4>", block_event)
root.bind("<Escape>", block_event)
root.bind("<Button>", block_event)
root.bind("<Key>", on_key)

root.focus_force()

r, g, b = 255, 0, 0
dr, dg, db = -1, 1, 1

label = tk.Label(
    root,
    text=TEXT,
    fg="white",
    font=("Arial", 40),
    justify="center"
)
label.pack(expand=True)

lock_terminal()
rgb_loop()
root.mainloop()
