import socket
import os
import sys
import time
from PIL import ImageTk
import PIL.Image
from _thread import *
import tkinter as tk
import pywinauto
import pyautogui
from settings import settings
import win32api
import win32ui

class ReceiverMenuClass():
	def focusWindow(self, processId):
		app = pywinauto.application.Application()
		window = app.window_(handle=processId)
		window.Minimize()
		window.Maximize()
		window.SetFocus()

	def focusWindowNormal(self, processId):
		app = pywinauto.application.Application()
		window = app.window_(handle=processId)
		window.SetFocus()

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
			self.ReceiverSock.connect((settings.HOST,settings.PORT))
			self.l['text'] = """Welcome to the Receiver panel! \n\r If you see this message everything is OK! \r Server connection is made and waiting for commands! \r All the commands send from the server will run through this window. \n\r Couple notes: \r This window MUST be kept open. \r  If you close this window after the connection has been made to the server \r the SERVER MUST BE RESTARTED!"""
		
			while True:
				data = self.ReceiverSock.recv(1024)
				reply = B'OK...' + data
				self.l['text'] = """Welcome to the Receiver panel! \n\r If you see this message everything is OK! \r Server connection is made and waiting for commands! \r All the commands send from the server will run through this window. \n\r Couple notes: \r This window MUST be kept open. \r  If you close this window after the connection has been made to the server \r the SERVER MUST BE RESTARTED!"""
				if not data: 
					break
				print(data)

				###KINECT
				if data.decode() == "START_KINECT":
					if os.path.isfile("C:\\code\\kinect\\Kinect_PCD_writer.exe"):
						os.startfile('C:\code\kinect\Kinect_PCD_writer.exe')
					else:
						print("Kinect Executable was not found!")
				if data.decode() == "STOP_KINECT":
					os.system("TASKKILL /F /IM Kinect_PCD_writer.exe")
				if data.decode() == "START_KINECT_RECORD":
					#SendKeys.SendKeys("{F8}")
					#pyautogui.press('f8')
					#pyautogui.press('F8')
					PyCWnd1 = win32ui.FindWindow( None, "Vidofnir" )
					PyCWnd1.SetForegroundWindow()
					PyCWnd1.SetFocus()

					win32api.keybd_event(0x77, 0, )
					time.sleep(1)
					win32api.keybd_event(0x77, 0, 2 )
				if data.decode() == "STOP_KINECT_RECORD":
					PyCWnd1 = win32ui.FindWindow( None, "Vidofnir" )
					PyCWnd1.SetForegroundWindow()
					PyCWnd1.SetFocus()

					win32api.keybd_event(0x78, 0, )
					time.sleep(1)
					win32api.keybd_event(0x78, 0, 2 )
				### OLD
				if data.decode() == "STARTALL":
					os.startfile('C:\\silverfit\\SilverFit-3.0.2.10380\\Games\\PuzzleGame\\PuzzleGame.exe')
					os.startfile('C:\\Program Files (x86)\\OBS\\OBS.exe')
				if data.decode() == "QUIT":
					os.system("TASKKILL /F /IM OBS.exe")
					os.system("TASKKILL /F /IM SilverFit.exe")
					os.system("TASKKILL /F /IM puzzlegame.exe")
				if data.decode() == "QUITGAME":
					os.system("TASKKILL /F /IM SilverFit.exe")
					os.system("TASKKILL /F /IM puzzlegame.exe")

				### special
				if data.decode() == "CLICK":
					pyautogui.click(550, 300, button='left')
				if data.decode() == "CLICK2":
					pyautogui.click(700, 700, button='left')
				if data.decode() == "HK_ENTER":
					pyautogui.press('enter')
				
				### Puzzlegame
				if data.decode() == "START_GAME":
					if os.path.isfile("C:\\silverfit\\SilverFit-3.0.2.10380\\Games\\PuzzleGame\\PuzzleGame.exe"):
						#os.system("start cmd /C \"cd C:\\silverfit\\SilverFit-3.0.2.10380\\Games\\PuzzleGame\" & PuzzleGame.exe")
						os.startfile('C:\silverfit\SilverFit-3.0.2.10380\Games\PuzzleGame\PuzzleGame.exe')
						print("Puzzle game should be starting?")
					else:
						print("Puzzle game was not found on the specified location.")
				if data.decode() == "STOP_GAME":
					os.system("TASKKILL /F /IM puzzlegame.exe")


				### GAMECAPTURE
				if data.decode() == "START_OBS":
					if os.path.isfile("C:\\Program Files (x86)\\OBS\\OBS.exe"):
						os.startfile('C:\Program Files (x86)\OBS\OBS.exe')
					else:
						print("OBS executable not found! \rMake sure the following exists: \rC:\\Program Files (x86)\\OBS\\OBS.exe\r\nPerhaps reinstall OBS?")
				if data.decode() == "STOP_OBS":
					os.system("TASKKILL /F /IM OBS.exe")
				if data.decode() == "START_EXERGAME_RECORD":
					pyautogui.press('f10')
				if data.decode() == "STOP_EXERGAME_RECORD":
					pyautogui.press('f11')


				### FORCEPLATES
				if data.decode() == "START_BIOWARE":
					if os.path.isfile("C:\\Program Files (x86)\\Kistler\\BioWare\\BioWare.exe"):
						os.startfile('C:\Program Files (x86)\Kistler\BioWare\BioWare.exe')
					else:
						print("Bioware was not found!")
				if data.decode() == "STOP_BIOWARE":
					os.system("TASKKILL /F /IM BioWare.exe")

				if data.decode() == "PRESTART_FP":
					try:
						Bioware = pywinauto.findwindows.find_windows(title='BioWare')
						if(len(Bioware) != 0):
							temp = max(Bioware)
							self.focusWindow(temp)
							pyautogui.hotkey('alt','a')
					except:
						print("Bioware not started?")
				if data.decode() == "START_FP_RECORD":
					try:
						Bioware = pywinauto.findwindows.find_windows(title='BioWare')
						if(len(Bioware) != 0):
							temp = max(Bioware)
							self.focusWindow(temp)
							pyautogui.press('enter')
					except:
						print("Bioware not started?")
				if data.decode() == "STOP_FP_RECORD":
					try:
						Bioware = pywinauto.findwindows.find_windows(title='BioWare')
						if(len(Bioware) != 0):
							temp = max(Bioware)
							self.focusWindow(temp)
							pyautogui.press('esc')
					except:
						print("Bioware not started?")

				
		#	self.l['text']="Sorry, i can't connect to the server. Is the server running? Is the server IP set & is my IP set?"
		except ConnectionRefusedError as error:
			self.l['text']="Sorry, i can't connect to the server. Is the server running? Is the server IP set & is my IP set?"
		except ConnectionAbortedError as error:
			print("Connection was forcible dropped. And there is nowhere to display the message.")
			self.ReceiverSock.close()
			self.close_window()
		except ConnectionResetError as error:
			self.l['text']="The connection with the server was reset and lost!"
		self.ReceiverSock.close()
