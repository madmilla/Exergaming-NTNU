# client.py
#
# @author: L. Veenendaal

import socket
import os
import pyautogui
"""

This client is just used for manually starting applications.
Still needs programming to make it start certain things or retrieve status of things.

"""
s = socket.socket()
s.connect(('10.20.185.93',443))
#s.connect(('10.0.0.1',8888))
while True:

	#command = input("Orders?\r\n")
	#s.send(command.encode())

	data = s.recv(1024)
	#reply = B'OK...' + data
	if not data: 
		break
	print(data)
	if data.decode() == "BOOT":
		if os.path.isfile("C:\\Program Files (x86)\\obs-studio\\bin\\64bit\\Obs64.exe"):
			os.system("start cmd /C \"cd \"C:\\Program Files (x86)\\obs-studio\\bin\\64bit\" & \"Obs64.exe\" ")#& \"exit\"
			#client.updateValue("action", 1)
			#client.sendByte(B"GAMECAPTURE - OBS Online")
		else:
			print("OBS executable not found! \r\nMake sure the following exists: \r\nC:\\Program Files (x86)\\obs-studio\\bin\\64bit\\Obs64.exe\r\nPerhaps reinstall OBS?")
			#client.updateValue("state", 1)
			#client.sendByte(B"GAMECAPTURE - OBS executable not found!")
	if data.decode() == "QUIT":
		os.system("TASKKILL /F /IM Obs64.exe")
	if data.decode() == "QQQQ":
		pyautogui.click(100, 100)
	if data.decode() == "WWWW":
		pyautogui.press('f10')
	if data.decode() == "EEEE":
		pyautogui.press('f11') 
s.close()