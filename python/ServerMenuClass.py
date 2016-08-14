import socket
import os
import sys
import pyautogui
from PIL import ImageTk
import PIL.Image
import threading
from _thread import *
import tkinter as tk

from settings import settings

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
