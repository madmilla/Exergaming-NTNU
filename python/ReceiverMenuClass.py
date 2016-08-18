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
import win32con
import win32ui
import re

class WindowMgr():
    """Encapsulates some calls to the winapi for window management"""
    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name = None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

class ReceiverMenuClass():
	def click(self,x,y):
		win32api.SetCursorPos((x,y))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
		time.sleep(0.2)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
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
	
		#self.ReceiverSock = socket.socket()
		#self.ReceiverSock.connect((settings.HOST,settings.PORT))
		HOST, PORT = "10.0.0.1", 443
		self.ReceiverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ReceiverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		#try:
		# Connect to server and send data
		
		

		# Receive data from the server and shut down
		#received = str(self.ReceiverSock.recv(1024), "utf-8")
		#finally:
		    #self.sock.close()

		#print("Sent:     {}".format(data))
		
		self.l['text'] = """Welcome to the Receiver panel! \n\r If you see this message everything is OK! \r Server connection is made and waiting for commands! \r All the commands send from the server will run through this window. \n\r Couple notes: \r This window MUST be kept open. \r  If you close this window after the connection has been made to the server \r the SERVER MUST BE RESTARTED!"""
		try:
			self.ReceiverSock.connect((HOST, PORT))
			self.ReceiverSock.sendall(bytes("online\n", "utf-8"))
			print('1')
			while True:
				data = str(self.ReceiverSock.recv(1024), "utf-8")
				print('3')
				
				#data = self.ReceiverSock.recv(1024)
				print("Received: {}".format(data))
				self.l['text'] = """Welcome to the Receiver panel! \n\r If you see this message everything is OK! \r Server connection is made and waiting for commands! \r All the commands send from the server will run through this window. \n\r Couple notes: \r This window MUST be kept open. \r  If you close this window after the connection has been made to the server \r the SERVER MUST BE RESTARTED!"""
				if data == b'':
					break
				if data == b'online\n': 
					break
				print(data + ' ? ' + 'START_KINECT')

				
				#if socket.gethostbyname(socket.gethostname()) == "10.0.0.1":
					###KINECT
				'''
				if data == "START_KINECT":
					if os.path.isfile("C:\\code\\kinect\\Kinect_PCD_writer.exe"):
						os.startfile('C:\code\kinect\Kinect_PCD_writer.exe')
					else:
						print("Kinect Executable was not found!")
				if data == "STOP_KINECT":
					os.system("TASKKILL /F /IM Kinect_PCD_writer.exe")
				if data == "START_KINECT_RECORD":
					try:
						PyCWnd1 = win32ui.FindWindow( None, "Vidofnir" )
						PyCWnd1.SetForegroundWindow()
						PyCWnd1.SetFocus()
						win32api.keybd_event(0x75, 0, ) #F6
						time.sleep(1)
						win32api.keybd_event(0x75, 0, 2 )
					except:
						print("Kinect Viewer is not open?")
				if data == "STOP_KINECT_RECORD":
					try:
						PyCWnd1 = win32ui.FindWindow( None, "Vidofnir" )
						PyCWnd1.SetForegroundWindow()
						PyCWnd1.SetFocus()
						win32api.keybd_event(0x76, 0, ) #F7
						time.sleep(1)
						win32api.keybd_event(0x76, 0, 2 )
					except:
						print("Kinect Viewer is not open?")
				'''

				

				### special
				#if socket.gethostbyname(socket.gethostname()) != "10.0.0.1":
				if data == "OPEN_BLACK_IMAGE":
					try:
						os.startfile("c:\\code\\python\\momentofzen\\black.png")
						time.sleep(1)
						pyautogui.press('f11')
					except:
						print("Black image not found. See if the is a folder and file in the python folder: momentofzen\\black.png")
				if data == "CLOSE_BLACK_IMAGE":
					try:
						PyCWnd1 = win32ui.FindWindow( None, "Photo Viewer Slide Show" )
						PyCWnd1.SetForegroundWindow()
						win32api.keybd_event(0x1B, 0, )
						time.sleep(1)
						win32api.keybd_event(0x1B, 0, 2 )
						PyCWnd1 = win32ui.FindWindow( None, "black.png - Windows Photo Viewer" )
						PyCWnd1.SetForegroundWindow()
						win32api.keybd_event(0x12, 0, )
						win32api.keybd_event(0x73, 0, )
						time.sleep(1)
						win32api.keybd_event(0x12, 0, 2 )
						win32api.keybd_event(0x73, 0, 2 )
					except:
						print("no slideshow found?")
				if data == "START_CLOCK":
					if os.path.isfile("C:\\code\\python\\clock2.py"):
						os.startfile('c:\code\python\clock2.py')
					else:
						print("Clock.py missing from the python folder.")
				if data == "STOP_CLOCK":
					os.system("TASKKILL /F /IM clock.py")

				if data == "GOBACK":
					Bioware = pywinauto.findwindows.find_windows(title='PuzzleGame')
					if(len(Bioware) != 0):
						temp = max(Bioware)
						app = pywinauto.application.Application()
						window = app.window_(handle=temp)
						window.SetFocus()
						pyautogui.click(1797,897)
				if data == "PEACOCK":
					Bioware = pywinauto.findwindows.find_windows(title='PuzzleGame')
					if(len(Bioware) != 0):
						temp = max(Bioware)
						app = pywinauto.application.Application()
						window = app.window_(handle=temp)
						window.SetFocus()
						timeout = 5   # [seconds]
						timeout_start = time.time()
						pyautogui.click(105,551)
						while time.time() < timeout_start + timeout:
						    pyautogui.moveTo(530,130)
						    pyautogui.moveTo(530,131)
						pyautogui.moveTo(105,551)
						for x in range(16):
							print("FUCK")
							#pyautogui.moveTo(105,551)
							win32api.keybd_event(0x27, 0, )
							time.sleep(0.1)
							#pyautogui.moveTo(105,550)
							win32api.keybd_event(0x27, 0, 2 )
							time.sleep(0.1)
							pass
				if data == "FLOWERBED":

					Bioware = pywinauto.findwindows.find_windows(title='PuzzleGame')
					if(len(Bioware) != 0):
						temp = max(Bioware)
						app = pywinauto.application.Application()
						window = app.window_(handle=temp)
						window.SetFocus()
						timeout = 5   # [seconds]
						timeout_start = time.time()
						pyautogui.click(1360,917)
						while time.time() < timeout_start + timeout:
						    pyautogui.moveTo(951,1136)
						    pyautogui.moveTo(951,1135)
						pyautogui.moveTo(1360,917)
						for x in range(2):
							print("MEW")
							#pyautogui.moveTo(105,551)
							win32api.keybd_event(0x25, 0, )
							time.sleep(0.2)
							#pyautogui.moveTo(105,550)
							win32api.keybd_event(0x25, 0, 2 )
							time.sleep(0.2)
							pass
				if data == "END_PUZZLE":
					import ctypes

					# see http://msdn.microsoft.com/en-us/library/ms646260(VS.85).aspx for details
					#ctypes.windll.user32.SetCursorPos(1800, 20)
				#	ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
				#	ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up
					#pyautogui.click(1800, 500, button='left')
					self.click(1800,500)
					time.sleep(0.5)
					self.click(1800,600)
					#pyautogui.click(1800, 600, button='left')

					#pyautogui.click(700, 700, button='left')
				if data == "HK_ENTER":
					pyautogui.press('enter')
			
				### OLD
				if data == "STARTALL":
					os.startfile('C:\\silverfit\\SilverFit-3.0.2.10380\\Games\\PuzzleGame\\PuzzleGame.exe')
					os.startfile('C:\\Program Files (x86)\\OBS\\OBS.exe')
				if data == "QUIT":
					os.system("TASKKILL /F /IM OBS.exe")
					os.system("TASKKILL /F /IM SilverFit.exe")
					os.system("TASKKILL /F /IM puzzlegame.exe")
				if data == "QUITGAME":
					os.system("TASKKILL /F /IM SilverFit.exe")
					os.system("TASKKILL /F /IM puzzlegame.exe")

				### Puzzlegame
				if data == "START_GAME":
					if os.path.isfile("C:\\Users\\bevguest\\Desktop\\test.bat"):
						#os.system("start cmd /C \"cd C:\\silverfit\\SilverFit-3.0.2.10380\\Games\\PuzzleGame\" & PuzzleGame.exe")
						os.startfile('C:\\Users\\bevguest\\Desktop\\test.bat')
						print("Puzzle game should be starting?")
					else:
						print("Puzzle game was not found on the specified location.")
					#if os.path.isfile("C:\\silverfit\\SilverFit-3.0.2.10380\\Games\\PuzzleGame\\PuzzleGame.exe"):
					#	#os.system("start cmd /C \"cd C:\\silverfit\\SilverFit-3.0.2.10380\\Games\\PuzzleGame\" & PuzzleGame.exe")
					#	os.startfile('C:\silverfit\SilverFit-3.0.2.10380\Games\PuzzleGame\PuzzleGame.exe')
					#	print("Puzzle game should be starting?")
					#else:
					#	print("Puzzle game was not found on the specified location.")
				if data == "START_GAME_TO":
					#try:
					PuzzleGame = pywinauto.findwindows.find_windows(title='PuzzleGame')
					if(len(PuzzleGame) != 0):
						temp = max(PuzzleGame)
						app = pywinauto.application.Application()
						window = app.window_(handle=temp)
						window.Minimize()
						window.Maximize()
						time.sleep(2)
						#pyautogui.click(421, 414, button='left')
						self.click(421,414)#NC
						#time.sleep(2)
						#win32api.keybd_event(0x0D, 0, ) #F6
						#time.sleep(2)
						#win32api.keybd_event(0x0D, 0, 2 )
					#except:
					#	print("PuzzleGame not found")
				if data == "START_GAME_FL":
					#try:
					PuzzleGame = pywinauto.findwindows.find_windows(title='PuzzleGame')
					if(len(PuzzleGame) != 0):
						temp = max(PuzzleGame)
						app = pywinauto.application.Application()
						window = app.window_(handle=temp)
						window.Minimize()
						window.Maximize()
						time.sleep(2)
						win32api.keybd_event(0x0D, 0, ) #F6
						time.sleep(2)
						win32api.keybd_event(0x0D, 0, 2 )
					#except:
					#	print("PuzzleGame not found")
				if data == "STOP_GAME":
					os.system("TASKKILL /F /IM puzzlegame.exe")


				### GAMECAPTURE
				if data == "START_OBS":
					if os.path.isfile("C:\\Program Files (x86)\\OBS\\OBS.exe"):
						os.startfile('C:\Program Files (x86)\OBS\OBS.exe')
					else:
						print("OBS executable not found! \rMake sure the following exists: \rC:\\Program Files (x86)\\OBS\\OBS.exe\r\nPerhaps reinstall OBS?")
				if data == "STOP_OBS":
					os.system("TASKKILL /F /IM OBS.exe")
				if data == "START_EXERGAME_RECORD":
					pyautogui.press('f10')
				if data == "STOP_EXERGAME_RECORD":
					pyautogui.press('f11')


				### FORCEPLATES
				if data == "START_BIOWARE":
					if os.path.isfile("C:\\Program Files (x86)\\Kistler\\BioWare\\BioWare.exe"):
						os.startfile('C:\Program Files (x86)\Kistler\BioWare\BioWare.exe')
					else:
						print("Bioware was not found!")
				if data == "STOP_BIOWARE":
					os.system("TASKKILL /F /IM BioWare.exe")

				if data == "PRESTART_FP":
					try:
						Bioware = pywinauto.findwindows.find_windows(title='BioWare')
						if(len(Bioware) != 0):
							temp = max(Bioware)
							self.focusWindow(temp)
							pyautogui.hotkey('alt','a')
					except:
						print("Bioware not started?")
				if data == "START_FP_RECORD":
					try:
						Bioware = pywinauto.findwindows.find_windows(title='BioWare')
						if(len(Bioware) != 0):
							temp = max(Bioware)
							self.focusWindow(temp)
							pyautogui.press('enter')
					except:
						print("Bioware not started?")
				if data == "STOP_FP_RECORD":
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
		finally:
			self.ReceiverSock.close()
				
