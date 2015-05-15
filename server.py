#!/usr/bin/python
import socket, sys, time, calendar
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
gameVariable = False
gameStartTime = -1 #time that the next game
shotFrequency = -1
stats = {}
team1 = {}
team2 = {}

def toEpoch(timestamp):
	split = str(timestamp).split(' ')
	tdate = map(int,split[1].split('-'))
	ttime = map(int,split[2].split(':'))
	tcode = (tdate[0], tdate[1], tdate[2], ttime[0], ttime[1], ttime[2])
	epoch = calendar.timegm(tcode)
	return (int(epoch))

def timeUntilNextGame():
	if gameStartTime != -1:
	    return str(gameStartTime - time.time())

def scheduleGame(gameStart, gameLength, gameStartTime, maxShots, shotFrequency):
	time.sleep(gameStart)
	startGame(gameLength, maxShots, shotFrequency)

def startGame(gameLength, maxShots, shotFrequency):
	global gameVariable
	gameVariable = True
	print "game started!"
	time.sleep(gameLength) #NOTE: Multiply by 60 later (convert to min)
	endGame()

def gameLogic():
	while 1:
		print "1. quit\n2. start game\n3. schedule game"
		command = input("Enter command: \n")
        	if int(command) == 1:
                	print "quit!"
			break
        	elif int(command) == 2:
                	gameLength = int(input("How long should this game last? (min) "))
			global maxShots
			maxShots = int(input("How many shots are allowed per player per game? "))
			global shotFrequency
			shotFrequency = int(input("How many shots are allowed per second? "))
			start_new_thread(startGame, (gameLength, maxShots, shotFrequency))
		elif int(command) == 3:
			gameStart = int(input("How long until next game starts? (min) "))
			gameStart *= 60
			global gameStartTime 
			gameStartTime= gameStart + time.time()
			gameLength = int(input("How long should this game last? (min) "))
			maxShots = int(input("How many shots are allowed per player per game? "))
			shotFrequency = int(input("How many shots are allowed per second? "))
			start_new_thread(scheduleGame, (gameStart, gameLength, gameStartTime, maxShots, shotFrequency))
		else:
		    print "You fail... Try 1-3."

def endGame():
	print "end game!"
	global gameVariable
	gameVariable = False

#Function for handling connections. This will be used to create threads
def clientthread(conn, username):
	#Sending message to connected client
	conn.send('Welcome to the server, '+username+'! Type something and hit enter!') #send only takes string

	#infinite loop so that function do not terminate and thread do not end.
	while True:

		#Receiving from client
		data = conn.recv(1024)
		global shotFrequency
		if not data:
			break
		global gameVariable
                if not gameVariable:
			#if timeUntilNextGame() != -1:
			#	conn.sendall("No game in progress. Next game starts in "+ timeUntilNextGame() + " seconds.")
			#else:
			#	conn.sendall("No game in progress.")
			break
		data = data.rstrip()
		print username+': '+data
		clientVariables = data.split(",") #client variables = splitted data
		if clientVariables[0] == "shot":
		   
		    if username in team1:
			if len(team1[username]["shots"]) < maxShots: 
			    if len(team1[username]["shots"]) == 0: 
				team1[username]["shots"].append(toEpoch(clientVariables[1]))
			    else:
				if int(toEpoch(clientVariables[1])) - int(team1[username]["shots"][-1]) >= shotFrequency:
		    			team1[username]["shots"].append(toEpoch(clientVariables[1]))
			else:
			    break
		    else:
			if len(team2[username]["shot"]) < maxShots:
			    if len(team2[username]["shots"]) == 0:
				team2[username]["shots"].append(toEpoch(clientVariables[1]))
			    else:
				if int(toEpoch(clientVariables[1])) - int(team2[username]["shots"][-1]) >= shotFrequency:
					team2[username]["shots"].append(toEpoch(clientVariables[1]))
			else:
			    break
		if clientVariables[0] == "hit":
		    if int(username)%2 == 1:	#if odd then
			if int(clientVariables[2])%2 != int(username)%2:
		    		team1[username]["hits"].append([toEpoch(clientVariables[1]),clientVariables[2]])
		    else:
			if int(clientVariables[2])%2 != int(username)%2:
		    		team2[username]["hits"].append([toEpoch(clientVariables[1]),clientVariables[2]])
		# print clientVariables[1] - team1[username]["shots"][-1]  
		# print shotFrequency
 		# print clientVariables[1] - team2[username]["shots"][-1]  
		# print shotFrequency

		print team1
		print team2
		print "Team 1 Stats: "
		for playerID in team1:
			print "Gun ",playerID,":" 
			print "     Shot count = ", len(team1[playerID]["shots"]) 
			print "     Hit count = ", len(team1[playerID]["hits"])
		print "Team 2 Stats: "
		for playerID2 in team2:
			print "Gun ",playerID2,":" 
			print "     Shot count = ", len(team2[playerID2]["shots"])
			print "     Hit count = ", len(team2[playerID2]["hits"])
		print
		
		if clientVariables[0] == "error":
		    	print "error"
			conn.sendall('got it!')


	#came out of loop
	conn.close()

#now keep talking with the client

start_new_thread(gameLogic, ()) #comma cause tuple

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
