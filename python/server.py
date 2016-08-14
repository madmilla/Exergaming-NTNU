import socket
import sys
import time
from _thread import *
HOST = '10.20.185.93'   # Symbolic name meaning all available interfaces
PORT = 443 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
CONNECTION_LIST = []
try:
    s.bind((HOST, PORT))
except socket.error as msg:
   # print('Bind failed. Error Code : ' + str(msg[0]) +'  Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')
 
s.listen(10)
print('Socket now listening')

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    #conn.send(B'Welcome to the server. Type something and hit enter\n') #send only takes string
    conn.send(B'XXXX') 
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client 
        print(10)
        time.sleep(2)
        print(10)
        conn.send(B'TEST')
        CONNECTION_LIST[0].send(B'TEST')
        broadcast_data(conn,B'TEST')
        data = conn.recv(1024)
        reply = B'_' + data
        if not data: 
            break
        broadcast_data(conn, data)
       # print(CONNECTION_LIST)
        CONNECTION_LIST[1].send(reply)
        conn.sendall(reply)
     
    #came out of loop
    conn.close()
 
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        try :
            socket.send(message)
        except :
            # broken socket connection may be, chat client pressed ctrl+c for example
            socket.close()
            CONNECTION_LIST.remove(socket)


#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    CONNECTION_LIST.append(conn)
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()