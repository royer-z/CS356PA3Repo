# Name: Royer V. Zamudio
# UCID: rvz2
# Section: 003

# Programming Assignment 3: Simple HTTP Client and Server using TCP sockets
# Client

import sys
from socket import *
import os.path, time

# Get command line arguments
argv = sys.argv
webURL = argv[1]
webURL = webURL.split('/') # https://www.w3schools.com/python/ref_string_split.asp
hostAndPort = webURL[0]
hostAndPort = hostAndPort.split(':')
host = hostAndPort[0]
if (host == "localhost"):
	host = "127.0.0.1"
port = hostAndPort[1]
host = host
port = int(port)
filename = webURL[1]
requestLen = 1000000

# Contact server
# Create socket containing server's IP address and process Port number
clientSocket = socket(AF_INET, SOCK_STREAM)
# Establish connection with server
clientSocket.connect((host, port))
# Bind socket (address, port)

cachedFile = False
try: # If cache exists
	cacheResult = open("cache.txt", "rt")

	for line in cacheResult:
		if (filename+"\n" == line):
			cachedFile = True
	cacheResult.close()

	if (cachedFile == False):
		# Prepare HTTP GET request
		requestGET = "GET /"+filename+" HTTP/1.1\r\nHost: "+host+":"+str(port)+"\r\n\r\n"

		# Send request to server
		clientSocket.send(requestGET.encode())

		# Receive response from server
		receivedData = clientSocket.recv(requestLen)

		# Process response
		receivedData = receivedData.decode()
		headerFormat = receivedData
		receivedData = receivedData.split('\r\n')
		statusLine = receivedData[0]
		statusLine = statusLine.split(' ')
		returnCode = statusLine[1]

		if (returnCode == "404"):
			print(requestGET)
			print(headerFormat)
		else:
			lastModLine = receivedData[2]
			lastModLine= lastModLine.split(': ')
			timePart = lastModLine[1]
			timePart = timePart.split('\r\n')
			timePart = timePart[0]
			
			bodyLine = receivedData[7]
			# Print file contents, and cache file
			print(bodyLine)
			fResult = open("cache.txt", "wt")
			fResult.write(filename+"\n"+timePart+"\n"+bodyLine)
			cacheResult.close()

		# Close socket
		clientSocket.close()
	else:
		# Prepare Coditional GET request
		cacheResult = open("cache.txt", "rt")
		saveNext = False
		for line in cacheResult:
			if (saveNext == True):
				last_mod_time = line
				saveNext = False
			if (filename+"\n" == line):
				saveNext = True
		cacheResult.close()

		requestGET = "GET /"+filename+" HTTP/1.1\r\nHost: "+host+":"+str(port)+"\r\nIf-Modified-Since: "+last_mod_time+"\r\n\r\n"

		# Send request to server
		clientSocket.send(requestGET.encode())

		# Receive response from server
		receivedData = clientSocket.recv(requestLen)

		# Process response
		receivedData = receivedData.decode()
		headerFormat = receivedData
		receivedData = receivedData.split('\r\n')
		statusLine = receivedData[0]
		statusLine = statusLine.split(' ')
		returnCode = statusLine[1]

		if (returnCode == "304"): # If file not modified
			print(requestGET)
			print(headerFormat)
			print("File has NOT been modified.")
		elif(returnCode == "404"): # If file not found
			print(requestGET)
			print(headerFormat)
		else: # Else print message, print file contents, and cache file
			print(requestGET)
			print(headerFormat)
			lastModLine = receivedData[2]
			lastModLine= lastModLine.split(': ')
			timePart = lastModLine[1]
			timePart = timePart.split('\r\n')
			timePart = timePart[0]

			bodyLine = receivedData[7]
			print("File has been modified.")
			print(bodyLine)
			fResult = open("cache.txt", "wt")
			fResult.write(filename+"\n"+timePart+"\n"+bodyLine)
			cacheResult.close()

		# Close socket
		clientSocket.close()

except IOError: # If cache does NOT exist
	# Create cache
	cacheResult = open("cache.txt", "wt")
	cacheResult.close()

	# Prepare HTTP GET request
	requestGET = "GET /"+filename+" HTTP/1.1\r\nHost: "+host+":"+str(port)+"\r\n\r\n"
	# Send request to server
	clientSocket.send(requestGET.encode())

	# Receive response from server
	receivedData = clientSocket.recv(requestLen)

	# Process response
	receivedData = receivedData.decode()
	headerFormat = receivedData
	receivedData = receivedData.split('\r\n')
	statusLine = receivedData[0]
	statusLine = statusLine.split(' ')
	returnCode = statusLine[1]

	if (returnCode == "404"):
		print(requestGET)
		print(headerFormat)
	else:	
		print(requestGET)
		print(headerFormat)
		lastModLine = receivedData[2]
		lastModLine= lastModLine.split(': ')
		timePart = lastModLine[1]
		timePart = timePart.split('\r\n')
		timePart = timePart[0]

		bodyLine = receivedData[7]
		# Print file contents, and cache file
		print(bodyLine)
		fResult = open("cache.txt", "wt")
		fResult.write(filename+"\n"+timePart+"\n"+bodyLine)
		cacheResult.close()

	# Close socket
	clientSocket.close()
