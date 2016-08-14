from time import sleep, strftime
from os import system
from datetime import datetime

def clear():
	system("clear")

def clock():
	while 1:
		try:
			clear()
			ctime = datetime.now()
			print(str(datetime.now()))
			sleep(0.001)
		except KeyboardInterrupt:
			clear()
			break

clock()