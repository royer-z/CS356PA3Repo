# Programming Assignment 3: Simple HTTP Client and Server using TCP sockets
# Client

import sys
from socket import *

# Get command line arguments
argv = sys.argv
webURL = argv[1]
webURL = webURL.split('/') # https://www.w3schools.com/python/ref_string_split.asp
hostAndPort = webURL[0]
hostAndPort = hostAndPort.split(':')
host = hostAndPort[0]
port = hostAndPort[1]
host = host
port = int(port)
filename = webURL[1]
requestLen = 1000000

# Contact server
# Create socket containing server's IP address and process Port number 
print("Creating socket.")
clientSocket = socket(AF_INET, SOCK_STREAM)
# Establish connection with server
print("Connecting.")
clientSocket.connect((host, port))
# Bind socket (address, port)

# Check if file is in Cache
try: # If file IS in Cache
	fResult = open(filename, "rt")
	print("File is in Cache.")

	# Prepare Coditional GET request
	requestGET = "requestGET"
	# Send request to server
	print("Sending data: ", requestGET)
	clientSocket.send(requestGET.encode())

	# Receive response from server
	print("Receiving.")
	receivedData = clientSocket.recv(requestLen)

	# Process response
	print("Received data: ", receivedData.decode())
	# If file not modified, print 'not modified' message
	# Else print 'modified' message, print file contents, and cache file
	

	# Close socket
	print("Closing.")
	clientSocket.close()

except IOError: # If file IS NOT in Cache
	print("File is not in Cache.")

	# Prepare HTTP GET request
	requestGET = "GET /"+filename+" HTTP/1.1\r\n"+"Host: "+host+":"+str(port)+"\r\n\r\n"
	# Send request to server
	print("Sending data: ") 
	print(requestGET)
	clientSocket.send(requestGET.encode())

	# Receive response from server
	print("Receiving.")
	receivedData = clientSocket.recv(requestLen)

	# Process response
	receivedData = receivedData.decode()
	print("Received data: ")
	print(receivedData)
	# Print file contents, and cache file

	# Close socket
	print("Closing.")
	clientSocket.close()
