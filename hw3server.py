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
print("Creating socket.")
serverSocket = socket(AF_INET, SOCK_STREAM)
# Bind socket (address, port)
print("Binding")
serverSocket.bind((serverIP, serverPort))
# Listening socket
print("Listening.")
serverSocket.listen(1)

# Receive request from client
while True:
	# Create a new socket to communicate with client
	# Accept connection with client
	print("Accepting.")
	connectionSocket, address = serverSocket.accept()
	# Receive request from client
	print("Receiving.")
	receivedData = connectionSocket.recv(responseLen)

	# Process request
	receivedData = receivedData.decode()
	receivedData = receivedData.split('\r\n')
	print("Received data split: ")
	print(receivedData)

	commandLine = receivedData[0].split(' ')
	command = commandLine[0]
	filename = commandLine[1]

	hostLine = receivedData[1]

	endLine = receivedData[2]

	print(command)
	print(filename)

	# Check if file exists
	try: # If file exists
		fResult = open(filename, "rt")
		content = fResult.read()
		print("File exists.")
		# Prepare HTTP GET response
		t = datetime.datetime.now(timezone.utc)
		date = time.strftime("%a, %d %b %Y %H:%M:%S %Z\r\n", t)

		secs = os.path.getmtime(filename)
		t2 = time.gmtime(secs)		
		last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", t2)

		dataLen = len(content)

		responseGET = "HTTP/1.1 200 OK\r\nDate: "+date+"\r\nLast-Modified: "+last_mod_time+"\r\nContent-Length: "+dataLen+"\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"+content

	except IOError: # If file does not exist
		print("File does NOT exist.")

	if (command == 'GET'):


	# Send response to client
	print("Sending data: ")
	print(responseGET)
	connectionSocket.send(responseGET.encode())

	# Close socket
	print("Closing.")
	connectionSocket.close()
