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

stats = {}
team1 = {}
team2 = {}

def gameLogic():
	while 1:
		print "1. quit\n2. start game"
		command = input("Enter command: ")
        	if int(command) == 1:
                	print "quit!"
			break
        	elif int(command) == 2:
                	gameLength = int(input("How long should this game last? (min) "))
                	print time.time()
			start_new_thread(startGame, (gameLength,))
			#maxshots = input("How many shots are allowed per player per game? ")
maxshots = 5
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
		clientVariables = data.split(",") #client variables = splitted data
		if clientVariables[0] == "shot":
		    if username in team1:
			if len(team1[username]["shots"]) <= maxshots:
		    		team1[username]["shots"].append(clientVariables[1])    
		    else:
			if len(team2[username]["shot"]) <= maxshots:
				team2[username]["shots"].append(clientVariables[1])
		if clientVariables[0] == "hit":
		    if int(username)%2 == 1:	#if odd then
			if int(clientVariables[2])%2 != int(username)%2:
		    		team1[username]["hits"].append([clientVariables[1],clientVariables[2]])
		    else:
			if int(clientVariable[2])%2 != int(username)%2:
		    		team2[username]["hits"].append([clientVariables[1],clientVariables[2]])
		print team1
		print team2
		if clientVariables[0] == "no game":
		    print "no game"
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
	stats[username] = {"shots":[],"hits":[]}
	if int(username)%2 == 1:
	    team1[username] = {"shots":[], "hits":[]}
	else:
	    team2[username] = {"shots":[], "hits":[]}
	print 'Connected with ' + addr[0] + ':' + str(addr[1])+' as '+username



	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
	start_new_thread(clientthread ,(conn, username))

s.close()
