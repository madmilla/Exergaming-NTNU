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
#s.connect(('10.20.185.93',443))
s.connect(('10.20.185.93',8888))
while True:

	#command = input("Orders?\r\n")
	#s.send(command.encode())

	data = s.recv(1024)
	#reply = B'OK...' + data
	if not data: 
		break
	print(data)
	if data.decode() == "EEGSTART":
		if os.path.isfile("C:\Program Files\Neuroscan\scan4.5\Acquire.exe"):
			os.system("start cmd /C \"cd \"C:\\Program Files\\Neuroscan\\scan4.5\" & \"Acquire.exe\" ")
	if data.decode() == "GAMESTARTALL":
		os.system("start cmd /C \"cd \"C:\\silverfit\\SilverFit-3.0.2.10380\\Games\\PuzzleGame\" & \"PuzzleGame.exe\" ")
		os.system("start cmd /C \"cd \"C:\\Program Files (x86)\\OBS\" & \"OBS.exe\" ")
	if data.decode() == "GAME":
		
		if os.path.isfile("C:\silverfit\SilverFit-3.0.2.10380\SilverFit.exe"):
			os.system("start cmd /C \"cd \"C:\\silverfit\\SilverFit-3.0.2.10380\" & \"SilverFit.exe\" ")
		#else:
			#s.send(B"GAME NOT FOUND")
	if data.decode() == "BOOT":
		if os.path.isfile("C:\\Program Files (x86)\\OBS\\OBS.exe"):
			os.system("start cmd /C \"cd \"C:\\Program Files (x86)\\OBS\" & \"OBS.exe\" ")
			#client.updateValue("action", 1)
			#client.sendByte(B"GAMECAPTURE - OBS Online")
		else:
			#s.send(B"OBS NOT FOUND")
			print("OBS executable not found! \r\nMake sure the following exists: \r\nC:\\Program Files (x86)\\obs-studio\\bin\\64bit\\Obs64.exe\r\nPerhaps reinstall OBS?")
			#client.updateValue("state", 1)
			#client.sendByte(B"GAMECAPTURE - OBS executable not found!")
	if data.decode() == "GAMESTOPALL":
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
s.close()