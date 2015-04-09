#!/usr/bin/python
import socket
import sys
from thread import *

HOST = ''	# Symbolic name meaning all available interfaces

try:
        PORT = int(sys.argv[1])	# Arbitrary non-privileged port
except:
        print 'ERROR, no port provided'
        sys.exit()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn, username):
	#Sending message to connected client
	conn.send('Welcome to the server, '+username+'! Type something and hit enter!') #send only takes string

	#infinite loop so that function do not terminate and thread do not end.
	while True:

		#Receiving from client
		data = conn.recv(1024)
		if not data:
			break
                data = data.rstrip()
		print username+': '+data
                conn.sendall('got it!')

	#came out of loop
	conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
	conn, addr = s.accept()
        #Get username from client
        username = conn.recv(1024)
        if not username:
                print('Username not recieved')
                break
        username = username.rstrip()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])+' as '+username

	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
	start_new_thread(clientthread ,(conn, username))

s.close()
