import socket
import os
import sys
import pyautogui
from PIL import ImageTk
import PIL.Image
from _thread import *
import tkinter as tk

class ReceiverMenuClass():
	def close_window(self):
		try:
			self.ReceiverSock.close()
		except ConnectionResetError as error:
			print("Connection already dropped")
		self.master.destroy()



	def __init__(self,master):
		self.master = master
		self.frame = tk.Frame(master)
		master.wm_title("Receiver")
		
		self.l = tk.Message(self.frame, text="Welcome to the Receiver panel! \n\r Currently trying to connect to the server")	
		self.l.pack()	
		self.button = tk.Button(self.frame, text="Close Window", command=self.close_window)
		self.button.pack()
		self.frame.pack()
		self.x = "Made by Lars Veenendaal" 
		start_new_thread(self.main, (self.x,))
		

	def main(self, x):
		try:
			self.ReceiverSock = socket.socket()
			self.ReceiverSock.connect(('10.20.185.93',443))
			self.l = tk.Message(self.frame, text="Welcome to the Receiver panel! \n\r If you see this message everything is OK! \n\r Server connection is made and waiting for commands! \n\r This window MUST be kept open. \n\r All the commands send from the server will run through this window.")
		
			#s.connect(('10.20.185.93',443))
		
			while True:
				#command = input("Orders?\r\n")
				#s.send(command.encode())

				data = self.ReceiverSock.recv(1024)
				#reply = B'OK...' + data
				if not data: 
					break
				print(data)
				if data.decode() == "STARTALL":
					os.system("start cmd /C \"cd \"C:\\silverfit\\SilverFit-3.0.2.10380\\Games\\PuzzleGame\" & \"PuzzleGame.exe\" ")
					os.system("start cmd /C \"cd \"C:\\Program Files (x86)\\OBS\" & \"OBS.exe\" ")
				if data.decode() == "GAME":
					if os.path.isfile("C:\\silverfit\\SilverFit-3.0.2.10380\\Games\\PuzzleGame\\PuzzleGame.exe"):
						os.system("start cmd /C \"cd \"C:\\silverfit\\SilverFit-3.0.2.10380\\Games\\PuzzleGame\" & \"PuzzleGame.exe\" ")
				if data.decode() == "BOOT":
					if os.path.isfile("C:\\Program Files (x86)\\obs-studio\\bin\\64bit\\Obs64.exe"):
						os.system("start cmd /C \"cd \"C:\\Program Files (x86)\\OBS\" & \"OBS.exe\" ")
						#client.updateValue("action", 1)
						#client.sendByte(B"GAMECAPTURE - OBS Online")
					else:
						print("OBS executable not found! \r\nMake sure the following exists: \r\nC:\\Program Files (x86)\\obs-studio\\bin\\64bit\\Obs64.exe\r\nPerhaps reinstall OBS?")
				if data.decode() == "QUIT":
					os.system("TASKKILL /F /IM OBS.exe")
					os.system("TASKKILL /F /IM SilverFit.exe")
					os.system("TASKKILL /F /IM puzzlegame.exe")
				if data.decode() == "QUITGAME":
					os.system("TASKKILL /F /IM SilverFit.exe")
					os.system("TASKKILL /F /IM puzzlegame.exe")
				if data.decode() == "CLICK":
					pyautogui.click(550, 300, button='left')
				if data.decode() == "CLICK2":
					pyautogui.click(700, 700, button='left')
				if data.decode() == "RECORD":
					pyautogui.press('f10')
				if data.decode() == "STOP":
					pyautogui.press('f11')
		#except OSError as error:
		#	self.l['text']="Sorry, i can't connect to the server. Is the server running? Is the server IP set & is my IP set?"
		except ConnectionRefusedError as error:
			self.l['text']="Sorry, i can't connect to the server. Is the server running? Is the server IP set & is my IP set?"
		except ConnectionAbortedError as error:
			print("Connection was forcible dropped. And there is nowhere to display the message.")
			close_window()
		except ConnectionResetError as error:
			self.l['text']="The connection with the server was reset and lost!"
		self.ReceiverSock.close()