#!/usr/bin/python

##
##	CSE 545 - Spring 2018
##	Team 9: Black Shadow (blackshadow@asu.edu)
##

'''------------------------------------------------------------------------------------------------------------------
 ' Port Scanner for Final - Project CTF
 '
 ' Group:	Black Shadow
 ' Team:	9
 ' Class: 	Spring 2018 CSE 545
 ' Professor:	Adam Doupe
 ' Date:	4/30/18
 '
 ' 
 ' Description: This application tries to bind a raw socket with every port to see if there is a resonse.
 '
 '
-----------------------------------------------------------------------------------------------------------------'''

# Configure port scanner. ##########################################################################################


#PORT_RANGE_LOW = 1024
#PORT_RANGE_HIGH = 49151
PORT_RANGE_LOW = 20000
PORT_RANGE_HIGH = 30000

TEAMS_TO_SCAN = ["team1"]#, "team2", "team3", "team4", "team5", "team6", "team7", "team8", "team10", "team11",
		    #"team12", "team13", "team14", "team15", "team16", "team17", "team18", "team19", "team20", "team21"]

####################################################################################################################

# Checks port if socket can make a connection.
def checkVerifyFlag(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((host,port))
	sock.close()
	return result==0


def main():
	print ("Starting scanner.")
	for host in TEAMS_TO_SCAN:
		print ("Scanning host: " + host)
		for x in range(PORT_RANGE_LOW, PORT_RANGE_HIGH):
			print ("Scanning port: " + str(x) + ", Open? " + checkVerifyFlag(host, x))
			

if __name__ == "__main__":	
	
	try:
		main()

	except:
		print ("Exception!")
