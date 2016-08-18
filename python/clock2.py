# Main.py
#
# @author: L. Veenendaal

import tkinter as tk
from time import sleep, strftime
from os import system
from datetime import datetime


def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("400x30+000+000")


if __name__ == "__main__":
	root = tk.Tk()
	root.title("window")
	root.wm_title("The Clock")

	frame = tk.Frame(root)
	frame.option_add("*background", "black")
	frame.option_add("*foreground", "white")
	l = tk.Message(root, text="Clock", font=("Helvetica", 14),width=400)
	l.pack(fill = "both", expand = "yes")
	frame.pack()
	center(root)

	while 1:
		try:
			root.update()
			ctime = datetime.now()
			l['text'] = str(datetime.now())
			sleep(0.02)
		except:
			print("Clock closed")
			exit()