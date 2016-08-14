import socket
import os
import sys
import pyautogui
from PIL import ImageTk
import PIL.Image
from _thread import *
import tkinter as tk
#from tkinter import *

class mainMenuClass():
	###########################################
	# DEFINES
	###########################################


	### IP BLOCK
	def openIPSettings(self):
		print('Button is pressed!')

		self.newWindow = tk.Toplevel(self.master)
		self.app = ipMenuClass(self.newWindow)
		
	def openServerPanel(self):
		print('Button is pressed!')

		self.newWindow = tk.Toplevel(self.master)
		self.app = ServerMenuClass(self.newWindow)

	def openReceiverPanel(self):
		print('Button is pressed!')

		self.newWindow = tk.Toplevel(self.master)
		self.app = ReceiverMenuClass(self.newWindow)

	def credits(self):
		popup = tk.Tk()
		popup.wm_title("About")
		msg = "Build for: \nNTNU exergaming project.\n Made by: \nLars Veenendaal\nmadmilla@gmail.com\n 2016"
		label = tk.Label(popup, text=msg)
		label.pack(side="top", fill="x", pady=10)
		B1 = tk.Button(popup, text="Close", command = popup.destroy)
		B1.pack()
		popup.mainloop()

	###########################################
	# Button placements
	###########################################
	def __init__(self,master):
		self.master = master
		self.frame = tk.Frame(master)

		#self.frame["bg"]="white"
		#self.frame.configure(background='white')
		self.frame.option_add("*background", "white")

		fp = open("logo_ntnu.png","rb")
		#fp = open("NTNU-logo-300x300.png","rb")
		#fp = open("ntnu-221.jpg","rb")
		self.img = 	ImageTk.PhotoImage(PIL.Image.open(fp))
		
		self.panel = tk.Label(master, image = self.img)
		self.panel.pack(side = "top", fill = "both",  expand = "yes") #
		self.l = tk.Message(master, text="Welcome to the control panel! Please select a mode to run in.",width=200)
		self.l.pack(fill = "both", expand = "yes")
		self.B = tk.Button(master, text ="Start Server", command = self.openServerPanel)
		self.B.pack(fill = "both", expand = "yes")
		self.B = tk.Button(master, text ="Start Receiver", command = self.openReceiverPanel)
		self.B.pack(fill = "both", expand = "yes")
		self.B = tk.Button(master, text ="Change IP Settings", command = self.openIPSettings)
		self.B.pack(fill = "both", expand = "yes")
		self.l = tk.Button(master, text="2016", command = self.credits)
		self.l.pack(fill = "both", expand = "yes")
		self.frame.pack()
