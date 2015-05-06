#!/usr/bin/python
import socket, sys, time
from thread import *

# config = open(config.txt)


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


players = []
scores = {}

def gameLogic():
	while 1:
		print "1. exit\n2. start game"
		command = input("Enter command: ")
        	if int(command) == 1:
                	print "exit!"
			break
        	elif int(command) == 2:
                	gameLength = input("How long should this game last? (min) ")
                	print time.time()
			start_new_thread(startGame, (gameLength,))


def startGame(gameLength):
	print "gamestarted!"
	time.sleep(gameLength)
	endGame()

def endGame():
	print "endgame!"

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
		print players
		print scores
                conn.sendall('got it!')

	#came out of loop
	conn.close()

#now keep talking with the client

start_new_thread(gameLogic, ())

while 1:
    #wait to accept a connection - blocking call
	conn, addr = s.accept()
        #Get username from client
        username = conn.recv(1024)
        if not username:
                print('Username not recieved')
                break
        username = username.rstrip()
	players.append(username)
	scores[username] = 0
	print 'Connected with ' + addr[0] + ':' + str(addr[1])+' as '+username



	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
	start_new_thread(clientthread ,(conn, username))

s.close()
