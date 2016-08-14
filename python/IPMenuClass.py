import socket
import os
import sys
import pyautogui
from PIL import ImageTk
import PIL.Image
from _thread import *
import tkinter as tk

class ipMenuClass():
	def __init__(self , master):
		self.master = master
		self.frame = tk.Frame(master)
		master.wm_title("Kubrick IP Settings")
		master.geometry("350x300")
		#self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25 , command = self.close_window)
		#self.quitButton.pack()
		
		self.l = tk.Message(self.frame, text="Here you can set the IP address to the correct value.")
		self.l.pack()
		self.button = tk.Button(self.frame, text="Set SERVER IP", command=self.setStaticIP)
		self.button.pack()
		self.button = tk.Button(self.frame, text="Set Client1 IP", command=self.setClient1IP)
		self.button.pack()
		self.button = tk.Button(self.frame, text="Set Client2 IP", command=self.setClient2IP)
		self.button.pack()
		self.button = tk.Button(self.frame, text="Set Client3 IP", command=self.setClient3IP)
		self.button.pack()
		self.button = tk.Button(self.frame, text="Set Client4 IP", command=self.setClient4IP)
		self.button.pack()
		self.button = tk.Button(self.frame, text="Reset IP with DHCP", command=self.resetIP)
		self.button.pack()
		self.button = tk.Button(self.frame, text="Close Window", command=self.close_window)
		self.frame.pack()


	def close_window(self):
		self.master.destroy()

	def setStaticIP(self):
		self.master.wm_title("IP ADDRESS SET")
		os.system("python makeIPStatic.py server")
	def setClient1IP(self):
		os.system("python makeIPStatic.py client1")
	def setClient2IP(self):
		os.system("python makeIPStatic.py client2")
	def setClient3IP(self):
		os.system("python makeIPStatic.py client3")
	def setClient4IP(self):
		os.system("python makeIPStatic.py client4")
	def resetIP(self):
		os.system("python makeIPStatic.py dhcp")