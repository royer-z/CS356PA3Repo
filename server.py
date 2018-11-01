# Name: Royer V. Zamudio
# UCID: rvz2
# Section: 003

# Programming Assignment 3: Simple HTTP Client and Server using TCP sockets
# Server

from socket import *
import datetime, time
import os.path

serverIP = "127.0.0.1"
serverPort = 12000
responseLen = 1000000

# Welcome client contact
# Create socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# Bind socket (address, port)
serverSocket.bind((serverIP, serverPort))
# Listening socket
serverSocket.listen(1)

# Receive request from client
while True:
	# Create a new socket to communicate with client
	# Accept connection with client
	connectionSocket, address = serverSocket.accept()
	# Receive request from client
	receivedData = connectionSocket.recv(responseLen)

	# Process request
	receivedData = receivedData.decode()
	receivedData = receivedData.split('\r\n')
	commandLine = receivedData[0]
	commandLine = commandLine.split(' ')
	command = commandLine[0]
	filename = commandLine[1]

	hostLine = receivedData[1]

	endLine = receivedData[2]
	if (endLine == ''):
		conGET = False
	else:
		condPart = endLine.split(': ')
		condPart = condPart[0]
		if (condPart == "If-Modified-Since"):
			conGET = True

	# Check if file exists
	try: # If file exists
		tempfileN = filename[1:]
		fResult = open(tempfileN, "rt")
		content = fResult.read()
		# Prepare HTTP GET response
		
		if (conGET == False): # If GET request
			t = time.time()
			t = time.gmtime(t)
			date = time.strftime("%a, %d %b %Y %H:%M:%S %Z\r\n", t)
			
			secs = os.path.getmtime(tempfileN)
			t2 = time.gmtime(secs)	
			last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", t2)
			dataLen = len(content)
			responseGET = "HTTP/1.1 200 OK\r\nDate: "+date+"Last-Modified: "+last_mod_time+"\r\nContent-Length: "+str(dataLen)+"\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"+content

			# Send response to client
			connectionSocket.send(responseGET.encode())

			# Close socket
			connectionSocket.close()
		else: # If Conditional GET request

			# Check if file has been modified
			# Extract If-Modified-Since date and convert to tuple
			endLine = endLine.split(': ')
			datePart = endLine[1]
			t = time.strptime(datePart, "%a, %d %b %Y %H:%M:%S %Z\r\n")
			secs = time.mktime(t)
			# Get file's last modified time
			secs2 = os.path.getmtime(tempfileN)
			t2 = time.gmtime(secs2)

			# Compare times
			if (t2 > t): # If file has been modified
				# Prepare GET response
				t = time.time()
				t = time.gmtime(t)
				date = time.strftime("%a, %d %b %Y %H:%M:%S %Z\r\n", t)

				secs = os.path.getmtime(tempfileN)
				t2 = time.gmtime(secs)		
				last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", t2)

				dataLen = len(content)

				responseGET = "HTTP/1.1 200 OK\r\nDate: "+date+"Last-Modified: "+last_mod_time+"\r\nContent-Length: "+str(dataLen)+"\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"+content
			
				# Send response to client
				connectionSocket.send(responseGET.encode())
		
				# Close socket
				connectionSocket.close()
			else: # If file has NOT been modified
				# Prepare conditional GET response
				t = time.time()
				t = time.gmtime(t)
				date = time.strftime("%a, %d %b %Y %H:%M:%S %Z\r\n", t)

				responseGET = "HTTP/1.1 304 Not Modified\r\nDate: "+date+"\r\n\r\n"
				# Send response to client
				connectionSocket.send(responseGET.encode())
		
				# Close socket
				connectionSocket.close()
	except IOError: # If file does not exist
		
		# Prepare NOT FOUND response
		t = time.time()
		t = time.gmtime(t)
		date = time.strftime("%a, %d %b %Y %H:%M:%S %Z\r\n", t)
		
		responseGET = "HTTP/1.1 404 Not Found\r\nDate: "+date+"\r\n\r\n"	

		# Send response to client
		connectionSocket.send(responseGET.encode())
		
		# Close socket
		connectionSocket.close()
