# client.py
#
# @author: L. Veenendaal

"""

This client is just used for manually starting applications.
Still needs programming to make it start certain things or retrieve status of things.

"""

import socket
import os
import sys
import time
import pyautogui
from PIL import ImageTk
import PIL.Image
from _thread import *
import threading
import tkinter as tk

## OOP block
from MainMenuClass import MainMenuClass
from ReceiverMenuClass import ReceiverMenuClass
from ServerMenuClass import ServerMenuClass
from IPMenuClass import ipMenuClass
from settings import settings

import sadmin #Need UAC level raised for mouse controlling and IP address adjustment
import subprocess
import pywinauto

if __name__ == "__main__":
	#if not sadmin.isUserAdmin():
	#	sadmin.runAsAdmin() 		#Need raised UAC status for being able to control the mouse and keyboard
	root = tk.Tk()
	root.title("window")
	print(settings.HOST)

	cls = MainMenuClass(root)
	root.wm_title("Kubrick Controller")
	root.mainloop()

