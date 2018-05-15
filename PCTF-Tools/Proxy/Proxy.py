#!/usr/bin/python
'''------------------------------------------------------------------------------------------------------------------
 ' MITM Proxy for Final - Project CTF
 '
 ' Group:	Black Shadow
 ' Team:	9
 ' Class: 	Spring 2018 CSE 545
 ' Professor:	Adam Doupe
 ' Date:	3/22/18
 '
 ' 
 ' Description: This application acts as a man in the middle between the outside and our vulnerable
 '		service.
 '
 ' Instructions: Make sure this application is executable, owner is the same as original service
 '		 owner, and ".py" extension removed. I.e: if working as a MITM to protect service
 '		 named "backup" name this backup and name the original backup whatever. BE SURE
 ' 		 TO UPDATE CONFIGURATION BELOW SUCH THAT SETTINGS MATCH CURRENT SERVICE.
 '
-----------------------------------------------------------------------------------------------------------------'''

from __future__ import print_function
import sys
import os
import socket
from Q import *

# import PWN TOOLS LOGS and set logging.
os.environ["PWNLIB_SILENT"] = "1"
from pwn import *
# log levels: 'CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'NOTSET', 'WARN', 'WARNING'
#context.log_level = 'WARNING'

# Configure for specific service. ##################################################################################

# Original service name and current (renamed) service name.
SERVICE_NAME = "service"
SERVICE_ORIGINAL = "backup"
# Port number this service is running on.
SERVICE_PORT = 20002

#SERVICE_LOCATION = '/opt/ctf/' + SERVICE_ORIGINAL + '/ro/'
SERVICE_LOCATION = '/home/albert/PCTF/' + SERVICE_ORIGINAL + '/ro/'

# ERRORLEVEL 1. Sanitize input by escaping characters in this list.
BLACKLIST_CHAR_1 = ['~','!','@','$','%','^','*','(',')',';']
BLACKLIST_STR_1 = ['ls']

# ERRORLEVEL 2. Ignore input, send error back.
BLACKLIST_CHAR_2 = ['\\','&', "'", '"']
BLACKLIST_STR_2 = ['cat', 'nano', 'rm ']
LEVEL_2_ERROR = "Invalid input. Try again"

# ERRORLEVEL 3. Input is dangerous, yell at hacker and exit.
BLACKLIST_CHAR_3 = ['\x90','|']
BLACKLIST_STR_3 = {'/bin','/sh','/bash'}
LEVEL_3_ERROR = "Your computer has been encrypted, send team 9 1 bitcoin to decrypt."

# If input contains non-ascii character return this error level.
NON_ASCII_ERRORLEVEL = 3

# Set max size input allowed. If msg size is larger set max msg errorlevel.
MAX_MSG_SIZE = 20
MAX_MSG_ERRORLEVEL = 3

# Set to 0 during CTF!!! This will reveal debugging information.
DEBUG = 0
# SET TO 0 DURING CTF!!! This will bypass firewall "rules" for debugging/testing purposes.
BYPASS_ERRORLEVEL = 0

# Flag tag that comes before a successful flag.
FLAG_TAG = "FLG"
FLAG_REGEX = (r'FLG[0-9A-Za-z]{13}')
# Flag is searched using regex (1) or just used looking for FLAG_TAG (0). 
# Using regex might not catch all instances if regex is incorrect.
# Using flag tag might catch false positives.
SEARCH_FLAG_REG = 0

# Flag verification
# This will read all FlagIDs, Flag passwords, and Flags. Will check if flagID and flag password
#  were sent in the incoming messsages. If so, send flag. If not block flag.
# Note: This might be too CPU intensive, so if application is slowing down set to 0.
# Be sure to have refl.py running.
VERIFY_FLAG = 0
VERIFY_FLAG_PORT = 30001
VERIFY_FLAG_IP = "localhost"
VERIFY_FLAG_SPLIT = ":__SpLiT__:"

# Queue that holds user input.
globalQ = Queue()

# Home server running reflector
HOME_IP = "68.99.86.222"
REFLECT_PORT = 49999
REFLECT_ON = 0
####################################################################################################################

def reflector():
	conn = None
	try:
        	conn = remote(HOME_IP, REFLECT_PORT, timeout=0.1)
        	sendStr = str(globalQ.getItems()) + VERIFY_FLAG_SPLIT + str(SERVICE_PORT)
        	conn.send(sendStr)
		recv = conn.recv(timeout = 0.2);
		conn.close()
	
	except EOFError:
		if (conn==None):
			conn.close()

# 
def checkFlag(userOutput):
	try:
		conn = remote(VERIFY_FLAG_IP, VERIFY_FLAG_PORT, timeout=0.1)
		sendStr = str(globalQ.getItems()) + VERIFY_FLAG_SPLIT + userOutput
		conn.send(sendStr)
		recv = conn.recv(timeout = 0.2);
		conn.close()

		if recv:
			if (recv == "1"):
				return True

		return False
	except:
		return False


# Check output traffic, if flag tag is detected take note of this traffic using regular expression instead of verifying
#  remotly against actual flags.
def checkOutput(userOutput):
	flagDetect = ((bool(re.search(FLAG_REGEX, userOutput)) and SEARCH_FLAG_REG) or (FLAG_TAG in userOutput and not SEARCH_FLAG_REG))
	debug("Flag detected? " + userOutput + str(flagDetect))
	if flagDetect and DEBUG:
		debug("Flag detected!")
		debug("Input used to get flag:")
		if (DEBUG):
			for item in globalQ.getItems():
				debug(item)

	return flagDetect

# Print debug statements.
def debug(msg):
	if (DEBUG):
		print ("Debug: " + msg)

# Creates system temp file with unique name.
# Use these temp files for further analysis during CTF.
def createTempFile():
	(fd, filename) = tempfile.mkstemp(dir=SERVICE_LOCATION+"tmp/")
	tfile = os.fdopen(fd, "w")
	tfile.close()
	subprocess.Popen(["/bin/cat", filename]).wait()
	#os.remove(filename)
	return filename

# Redirect stdout to file specified or temp file.
def stdoutToFileOn(filename = ""):
	if (filename == ""):
		filename = createTempFile()
	original = sys.stdout
	sys.stdout = open(filename, 'w')
	return original

# Returns true if entire string is valid ASCII
# else return false
def isAscii(myStr):
	try:
		myStr.decode("ascii")
	except UnicodeDecodeError:
		return False
	else:
		return True

# Return level of severity based on input.
# 0. Input is Ok.
# 1. Input was sanitized.
# 2. Input was ignored, send error back.
# 3. Input was dangerous exit.
def checkInput(msg, counter):
	errorLevel = 0

	for key in BLACKLIST_STR_1:
		if key in msg:
			errorLevel = 1
	for key in BLACKLIST_STR_2:
		if key in msg:
			errorLevel = 2
	for key in BLACKLIST_STR_3:
		if key in msg:
			errorLevel = 3

	for c in msg:
		if (c in BLACKLIST_CHAR_1 and errorLevel < 1):
			errorLevel = 1
		if (c in BLACKLIST_CHAR_2 and errorLevel < 2):
			errorLevel = 2
		if (c in BLACKLIST_CHAR_3 and errorLevel < 3):
			errorLevel = 3

	if (not isAscii(msg) and errorLevel < NON_ASCII_ERRORLEVEL):
		errorLevel = NON_ASCII_ERRORLEVEL

	if (len(msg) > MAX_MSG_SIZE and errorLevel < MAX_MSG_ERRORLEVEL):
		errorLevel = MAX_MSG_ERRORLEVEL
	
	debug("Error level: " + str(errorLevel))

	return errorLevel

# Escapes characters in BLACKLIST_CHAR_1 with the '\' char.
def sanitizeInput(msg, errorLevel):
	for c in BLACKLIST_CHAR_1:
		msg = msg.replace(c, "\\"+c)

	debug(msg)
	return msg


# Redirect stdout to original
def stdoutToFileOff(originalStdOut):
	sys.stdout = originalStdOut


def main(p):

	debug ("In Main")
	#stdoutToFileOff(origOut)
	counter = 1

	# While process is not terminated.
	msg = ""
	while p.poll() == None:
		try:
			# keep receiving stdout of application until empty string is sent.
			tempRecv = p.recv(timeout=0.1)
			while tempRecv:
				msg += tempRecv
				tempRecv = p.recv(timeout=0.1)
		except:
			debug("Exception! 243")
			# If application has exit.
			if p.poll() != None:
				debug("Application has terminated")

				if (msg != None)  and (msg):
					# Check output
					validFlag = False
					if (VERIFY_FLAG and not SEARCH_FLAG_REG):
						validFlag = checkFlag(msg)
					if (SEARCH_FLAG_REG and not VERIFY_FLAG):
						validFlag = checkOutput(msg)

					if (validFlag):
						print(LEVEL_3_ERROR)
						sys.stdout.flush()
						break
					
					# prints stdout
					print(msg,end='')
					sys.stdout.flush()
			break

		# Check output
		validFlag = False
		if (VERIFY_FLAG and not SEARCH_FLAG_REG):
			validFlag = checkFlag(msg)
		if (SEARCH_FLAG_REG and not VERIFY_FLAG):
			validFlag = checkOutput(msg)

		if (validFlag):
			print(LEVEL_3_ERROR)
			sys.stdout.flush()
			break
		
		# prints stdout
		print(msg,end='')
		sys.stdout.flush()

		# gets input
		userIn = str(raw_input()).strip()
		globalQ.enQ(userIn)

		# Check error level then act accordingly.
		errorLevel = checkInput(userIn, counter)

		if (errorLevel == 1 and not BYPASS_ERRORLEVEL):
			userIn = sanitizeInput(userIn, errorLevel)
		elif (errorLevel == 2 and not BYPASS_ERRORLEVEL):
			print (LEVEL_2_ERROR)
			sys.stdout.flush()
			continue
		elif (errorLevel == 3 and not BYPASS_ERRORLEVEL):
			print(LEVEL_3_ERROR)
			sys.stdout.flush()
			break

		debug("Count " + str(counter))

		# sends user input to process
		p.sendline(userIn)
		counter+=1
		msg = ""

		# If application has exit.
		if p.poll() != None:
			debug("Application has terminated")
			try:
				msg = p.recvall()

			except:
				debug("Exception!")
			
			# Check output
			validFlag = False
			if (VERIFY_FLAG and not SEARCH_FLAG_REG):
				validFlag = checkFlag(msg)
			if (SEARCH_FLAG_REG and not VERIFY_FLAG):
				validFlag = checkOutput(msg)

			if (validFlag):
				print(LEVEL_3_ERROR)
				sys.stdout.flush()
				break

			if (msg != None) and (msg):
				print(msg,end='')
				sys.stdout.flush()
			
			break


	if (DEBUG):
		debug("\nStart of queue:")
		while (not globalQ.isEmpty()):
			debug("size: " + str(globalQ.size()))
			debug ("Input: " + str(globalQ.deQ()))
		debug ("end")


if __name__ == "__main__":	
	
	# Runs local process
	p = process(SERVICE_LOCATION + SERVICE_NAME)

	try:
		main(p)

	except KeyboardInterrupt:
		debug ("\nKeyboard Interrupt")
		if (VERIFY_FLAG): 
			validFlag = checkFlag("Keyboard Interrupt")

	except:
          debug ("\nexcept here")
          if VERIFY_FLAG:
			validFlag = checkFlag("Keyboard Interrupt2")

	finally:
		p.kill()
		debug("\nfinally")
		# Call reflector.
		if (REFLECT_ON):
			reflector()



