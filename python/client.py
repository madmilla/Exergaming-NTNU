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

#I higher UAC status for mouse controlling
import sadmin
import subprocess
import pywinauto
#from pywinauto.findwindows    import find_window
#from pywinauto.win32functions import SetForegroundWindow

class settings():
	#HOST = '192.168.137.116'
	HOST = '10.0.0.1'
	PORT = 443


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
		#os.system("python ReceiverClass.py")
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


class ReceiverMenuClass():
	def focusWindow(self, processId):
		app = pywinauto.application.Application()
		window = app.window_(handle=processId)
		window.Minimize()
		window.Maximize()
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
					if os.path.isfile("C:\\code\\pcd_write_test.exe"):
						os.startfile('C:\code\pcd_write_test.exe')
					else:
						print("Kinect Executable was not found!")
				if data.decode() == "STOP_KINECT":
					os.system("TASKKILL /F /IM pcd_write_test.exe")
				if data.decode() == "START_KINECT_RECORD":
					try:
						Kinect = pywinauto.findwindows.find_windows(title='Point Cloud Viewer')
						if(len(Kinect) != 0):
							temp = max(Kinect)
							self.focusWindow(temp)
							pyautogui.press('up')
					except:
						print("Kinect not started?")
				if data.decode() == "STOP_KINECT_RECORD":
					try:
						Kinect = pywinauto.findwindows.find_windows(title='Point Cloud Viewer')
						if(len(Kinect) != 0):
							temp = max(Kinect)
							self.focusWindow(temp)
							pyautogui.press('down')
					except:
						print("Kinect not started?")

				
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

class ServerMenuClass():
	### DEFINES
	def connectToServer(self):
		ServerMenuClass.serverSock = socket.socket()
		ServerMenuClass.serverSock.connect((settings.HOST,settings.PORT))

	def disconnectToServer():
		try:
			print("Set us back to hell")
			ServerMenuClass.Server_stop.set()
			ServerMenuClass.Client_stop.set()
			print("Close hell")
			ServerMenuClass.serverSock.close()
			self.l['text'] ="Welcome to the Server control panel! The server is no longer running!"
			print("Set us back to hell")
			ServerMenuClass.l2['text'] = 'Server closed'
			print("Set us back to hell")
			self.master.wm_title("OFF | Server Panel")
			print("Set us back to hell")
			self.startserver.configure(text = 'Start server',command = self.startServer)
			print("Set us back to hell")
		except:
			print("FUCK")


	### unneeded?
	def enterCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'HK_ENTER')

	### PRESTART
	def startOBSCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'START_OBS')
	def startGameCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'START_GAME')
	def startKinectCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'START_KINECT')
	def startBiowareCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'START_BIOWARE')
	def prestartForceplatesCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'PRESTART_FP')

	#RECORD
	def startRecordingCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'START_EXERGAME_RECORD')
	def stopRecordingCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'STOP_EXERGAME_RECORD')
	def startBiowareRecordingCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'START_FP_RECORD')
	def stopBiowareRecordingCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'STOP_FP_RECORD')
	def startKinectRecordingCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'START_KINECT_RECORD')
	def stopKinectRecordingCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'STOP_KINECT_RECORD')

	#Special Actions

	def clickCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'CLICK')
	def click2CallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'CLICK2')
	def testCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'TEST')
	def test2CallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'TEST2')

	###TERMINATE
	def stopGameCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'STOP_GAME')
	def stopBiowareCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'STOP_BIOWARE')
	def stopOBSCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'STOP_OBS')
	def stopKinectCallBack(self):
		self.broadcast_data(ServerMenuClass.serverSock,B'STOP_KINECT')


	def __init__(self,master):
		ServerMenuClass.conn = 0
		ServerMenuClass.CONNECTION_LIST = []
		ServerMenuClass.serverSock = 0

		self.master = master
		self.frame = tk.Frame(master)
		self.master.wm_title("OFF | Server Panel")
		self.l = tk.Message(master, text="Welcome to the Server control panel! The server is not yet running!",width="400").grid(row=0,columnspan=4)


		self.startserver = tk.Button(master, text ="Start the server", command = self.startServer)
		self.startserver.grid(row=1,columnspan=2)
		ServerMenuClass.l2 = tk.Message(master, text="Server is not started",width="200")
		ServerMenuClass.l2.grid(row=1, column=2,columnspan=2)
		#self.l2.
		self.l = tk.Label(master, text ="Prestart").grid(row=2,column=0)
		self.l = tk.Label(master, text ="Recording").grid(row=2,column=1)
		self.l = tk.Label(master, text ="Specials").grid(row=2,column=2)
		self.l = tk.Label(master, text ="Termination!").grid(row=2,column=3)

		#Prestart channel
		self.B = tk.Button(master, text ="Start Game", command = self.startGameCallBack).grid(row=3,column=0)
		self.B = tk.Button(master, text ="Start Game recording software", command = self.startOBSCallBack).grid(row=4,column=0)
		self.B = tk.Button(master, text ="Start Bioware", command = self.startBiowareCallBack).grid(row=5,column=0)
		self.B = tk.Button(master, text ="Hotkey (Hackaround):\nPrestart power-on for Forceplates", command = self.prestartForceplatesCallBack).grid(row=6,column=0)
		self.B = tk.Button(master, text ="Start Kinect", command = self.startKinectCallBack).grid(row=7,column=0)

		#Recording channel
		self.B = tk.Button(master, text ="Start game recording", command = self.startRecordingCallBack).grid(row=3,column=1)
		self.B = tk.Button(master, text ="Stop game recording", command = self.stopRecordingCallBack).grid(row=4,column=1)
		self.B = tk.Button(master, text ="Start BioWare Recording", command = self.startBiowareRecordingCallBack).grid(row=5,column=1)
		self.B = tk.Button(master, text ="Stop BioWare Recording", command = self.stopBiowareRecordingCallBack).grid(row=6,column=1)
		self.B = tk.Button(master, text ="Start Kinect Recording", command = self.startKinectRecordingCallBack).grid(row=7,column=1)
		self.B = tk.Button(master, text ="Stop Kinect Recording", command = self.stopKinectRecordingCallBack).grid(row=8,column=1)

		
		#Specials
		self.B = tk.Button(master, text ="Press enter", command = self.enterCallBack).grid(row=3,column=2)
		self.B = tk.Button(master, text ="Mouse 1", command = self.clickCallBack).grid(row=4,column=2)
		self.B = tk.Button(master, text ="Mouse 2", command = self.click2CallBack).grid(row=5,column=2)
		self.B = tk.Button(master, text ="TEST", command = self.testCallBack).grid(row=6,column=2)
		self.B = tk.Button(master, text ="TEST2", command = self.test2CallBack).grid(row=7,column=2)
		#self.B = tk.Button(master, text ="Stop everything", command = self.stopOBSCallBack).grid(row=8,column=2)
		#self.B = tk.Button(master, text ="Close window & Stop all", command = self.stopOBSCallBack).grid(row=9,column=2)

		#Terminate block
		"""
		self.B = tk.Button(master, text ="Quit PuzzleGame", command = self.stopGameCallBack).grid(row=3,column=3)
		self.B = tk.Button(master, text ="Quit OBS", command = self.stopOBSCallBack).grid(row=4,column=3)
		self.B = tk.Button(master, text ="Quit BioWare", command = self.stopBiowareCallBack).grid(row=5,column=3)
		self.B = tk.Button(master, text ="Quit Kinect (MIA)", command = self.stopKinectCallBack).grid(row=6,column=3)
		"""
	def startServer(self):

		
		ServerMenuClass.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ServerMenuClass.serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print('Socket created')
		try:
			ServerMenuClass.serverSock.bind((settings.HOST, settings.PORT))
			ServerMenuClass.l2['text'] = 'Server started!'
			print('Socket bind complete')
			ServerMenuClass.serverSock.listen(10)
			print('Socket now listening')
			ServerMenuClass.l2['text'] = 'Server is now listening'
			#self.l['text'] ="Welcome to the Server control panel! The server is RUNNING!"
			self.master.wm_title("ON | Server Panel")
			self.startserver.configure(text = 'Stop server',command = ServerMenuClass.disconnectToServer)
			self.x = "Made by Lars Veenendaal" 
			ServerMenuClass.Server_stop = threading.Event()
			ServerMenuClass.Client_stop = threading.Event()
			print('Socket now listening')
			self.Server = threading.Thread(target=ServerMenuClass.main, args=(1, ServerMenuClass.Server_stop))
			self.Server.daemon = True
			self.Server.start()
			ServerMenuClass.Server_stop.set()
			#self.Server_stop.clear()
			#self.Client_stop.clear()
		except socket.error as msg:
			ServerMenuClass.l2['text'] = 'Server Bind failed'
			ServerMenuClass.serverSock.close()
		     
		

	#Function for handling connectionserverSock. This will be used to create threads
	def clientthread(self, stop, conn):
		while(not stop.is_set()):
			try:
				#while(not stop_event.is_set()):
				#Sending message to connected client
				#conn.send(B'Welcome to the server. Type something and hit enter\n') #send only takes string
				ServerMenuClass.conn.send(B'XXXX') 
				#infinite loop so that function do not terminate and thread do not end.
				while True:
					#Receiving from client
					data = ServerMenuClass.conn.recv(1024)
					reply = B'_' + data
					if not data: 
						break
					broadcast_data(ServerMenuClass.conn, data)
					# print(CONNECTION_LIST)
					ServerMenuClass.CONNECTION_LIST[1].send(reply)
					ServerMenuClass.conn.sendall(reply)
					stop.wait(time)
					pass
				#came out of loop
			except ConnectionResetError as e:
				print("Receiver dropped the connection. Closing the connection.")
				ServerMenuClass.conn.close()
				ServerMenuClass.Client_stop.set()
			except ConnectionAbortedError as e:
				print("Receiver dropped the connection. Closing the connection.")
				ServerMenuClass.conn.close()
				ServerMenuClass.Client_stop.set()
	 
	def broadcast_data(self,sock, message):
		#Do not send the message to master socket and the client who has send us the message
		for socket in ServerMenuClass.CONNECTION_LIST:
			try:
				socket.send(message)
			except:
				# broken socket connection may be, chat client pressed ctrl+c for example
				socket.close()
				ServerMenuClass.CONNECTION_LIST.remove(socket)
		#now keep talking with the client
	def main(arg1, stop):

		while(not stop.is_set()):
			#wait to accept a connection - blocking call
			try:
				print("Y")
				ServerMenuClass.conn, addr = ServerMenuClass.serverSock.accept()
				print("Y")
				ServerMenuClass.CONNECTION_LIST.append(ServerMenuClass.conn)
				print('Connected with ' + addr[0] + ':' + str(addr[1]))
				
				#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
				#start_new_thread(self.clientthread ,(conn,))
				
				ServerMenuClass.client =threading.Thread(target=ServerMenuClass.clientthread, args=("ClientLoop", ServerMenuClass.Client_stop, ServerMenuClass.conn,))
				ServerMenuClass.client.daemon = True
				ServerMenuClass.client.start()

				stop.wait(time)
				#pass
			except OSError as error:
				ServerMenuClass.l2['text'] = 'Server stopped?'		
		#print("Server stopped")
		#ServerMenuClass.disconnectToServer()

	

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



if __name__ == "__main__":
	#if not sadmin.isUserAdmin():
	#	sadmin.runAsAdmin() 		#Need raised UAC status for being able to control the mouse and keyboard
	root = tk.Tk()
	root.title("window")
	print(settings.HOST)
	#root.geometry("350x300")

	cls = mainMenuClass(root)
	root.wm_title("Kubrick Controller")
	root.mainloop()

