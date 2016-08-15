# Main.py
#
# @author: L. Veenendaal

"""

This client is just used for manually starting applications.
Still needs programming to make it start certain things or retrieve status of things.

"""

import socket
import os
import sys
from PIL import ImageTk
import PIL.Image
import tkinter as tk

## OOP block
from MainMenuClass import MainMenuClass
from ReceiverMenuClass import ReceiverMenuClass
from ServerMenuClass import ServerMenuClass
from IPMenuClass import ipMenuClass
from settings import settings


if __name__ == "__main__":
	#if not sadmin.isUserAdmin():
	#	sadmin.runAsAdmin() 		#Need raised UAC status for being able to control the mouse and keyboard
	root = tk.Tk()
	root.title("window")
	print(settings.HOST)

	cls = MainMenuClass(root)
	root.wm_title("Ratatosk")
	root.mainloop()

