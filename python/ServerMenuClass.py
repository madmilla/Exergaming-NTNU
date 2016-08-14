import socket
import os
import sys
import pyautogui
from PIL import ImageTk
import PIL.Image
from _thread import *
import tkinter as tk

class ServerMenuClass():
	def connectToServer(self):
		ServerMenuClass.serverSock = socket.socket()
		ServerMenuClass.serverSock.connect(('10.20.185.93',443))

	def disconnectToServer(self):
		ServerMenuClass.serverSock.close()
		self.l['text'] ="Welcome to the Server control panel! The server is no longer running!"
		self.l2['text'] = 'Server closed'
		self.master.wm_title("OFF | Server Panel")
		self.startserver.configure(text = 'Start server',command = self.startServer)

	def startOBSCallBack(self):
		command = ("BOOT")
		self.broadcast_data(ServerMenuClass.serverSock, "BOOT")
		#self.s.send(command.encode())

	def stopOBSCallBack(self):
		command = ("QUIT")
		ServerMenuClass.serverSock.send(command.encode())

	def startGameCallBack(self):
		command = ("GAME")
		ServerMenuClass.serverSock.send(command.encode())

	def stopGameCallBack(self):
		command = ("QUITGAME")
		ServerMenuClass.serverSock.send(command.encode())

	def startRecordingCallBack(self):
		command = ("RECORD")
		ServerMenuClass.serverSock.send(command.encode())

	def stopRecordingCallBack(self):
		command = ("STOP")
		ServerMenuClass.serverSock.send(command.encode())

	def __init__(self,master):
		ServerMenuClass.conn = 0
		ServerMenuClass.CONNECTION_LIST = []
		ServerMenuClass.serverSock = 0

		self.master = master
		self.frame = tk.Frame(master)
		self.master.wm_title("OFF | Server Panel")

		ServerMenuClass.serverSock = 0
		self.l = tk.Message(master, text="Welcome to the Server control panel! The server is not yet running!",width="400")
		self.l.grid(row=0,columnspan=2)

		self.startserver = tk.Button(master, text ="Start the server", command = self.startServer)
		self.startserver.grid(row=1,column=0)
		self.l2 = tk.Message(master, text="Server is not started",width="200")
		self.l2.grid(row=1, column=1)
		#self.l2.
		
		self.B = tk.Button(master, text ="Start Game", command = self.startGameCallBack).grid(row=2,column=0)
		#self.B = tk.Button(master, text ="stop Game", command = self.stopGameCallBack).grid(row=3,column=0)
		self.B = tk.Button(master, text ="Start OBS", command = self.startOBSCallBack).grid(row=3,column=0)
		self.B = tk.Button(master, text ="Start game recording", command = self.startRecordingCallBack).grid(row=4,column=0)
		#self.B = tk.Button(master, text ="stop game recording", command = self.stopRecordingCallBack).grid(row=5,column=0)
		self.B = tk.Button(master, text ="Start Forceplate", command = self.startOBSCallBack).grid(row=5,column=0)
		self.B = tk.Button(master, text ="Start Kinect", command = self.startOBSCallBack).grid(row=6,column=0)
		self.B = tk.Button(master, text ="Stop everything", command = self.stopOBSCallBack).grid(row=7,column=0)
		self.B = tk.Button(master, text ="Close window & Stop all", command = self.stopOBSCallBack).grid(row=8,column=0)
		
		

	def startServer(self):
		HOST = '10.20.185.93'   # Symbolic name meaning all available interfaces
		PORT = 443 # Arbitrary non-privileged port
		
		ServerMenuClass.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ServerMenuClass.serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print('Socket created')
		try:
			ServerMenuClass.serverSock.bind((HOST, PORT))
			self.l2['text'] = 'Server started!'
			print('Socket bind complete')
			ServerMenuClass.serverSock.listen(10)
			print('Socket now listening')
			self.l2['text'] = 'Server is now listening'
			self.l['text'] ="Welcome to the Server control panel! The server is RUNNING!"
			self.master.wm_title("ON | Server Panel")
			self.startserver.configure(text = 'Stop server',command = self.disconnectToServer)
			self.x = "Made by Lars Veenendaal" 
		except socket.error as msg:
			self.l2['text'] = 'Server Bind failed'
			#sys.exit()
		     
		

	#Function for handling connectionserverSock. This will be used to create threads
	def clientthread(self,conn):
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
		#came out of loop
		ServerMenuClass.conn.close()
	 
	def broadcast_data(self,sock, message):
		#Do not send the message to master socket and the client who has send us the message
		for socket in ServerMenuClass.CONNECTION_LIST:
			if socket != ServerMenuClass.serverSock and socket != sock:
				try:
					socket.send(message)
				except:
					# broken socket connection may be, chat client pressed ctrl+c for example
					socket.close()
					ServerMenuClass.CONNECTION_LIST.remove(socket)
		#now keep talking with the client
	def main(self,x):
		while 1:
			#wait to accept a connection - blocking call
			ServerMenuClass.conn, addr = ServerMenuClass.serverSock.accept()
			ServerMenuClass.CONNECTION_LIST.append(ServerMenuClass.conn)
			print('Connected with ' + addr[0] + ':' + str(addr[1]))
			
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			start_new_thread(self.clientthread ,(ServerMenuClass.conn,))
		self.disconnectToServer()



root = tk.Tk()
root.title("window")
#root.geometry("350x300")

cls = ServerMenuClass(root)
root.wm_title("Kubrick Controller")
root.mainloop()

