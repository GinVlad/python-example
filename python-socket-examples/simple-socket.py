#!/usr/bin/python

import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socket.bind(("0.0.0.0", 8000))

socket.listen(1)

print "Waiting client..."
(client, (ip, port)) = socket.accept()

print "Receive connection from: " + str(ip)
print "Starting receive data..."
data = 'data'
while len(data):
	data = client.recv(2048)
	print "Client sent: " + data
	client.send("You said: "+data) #Send data to client

print "Closing connection..."
client.close()

print "Server close..."
socket.close()

