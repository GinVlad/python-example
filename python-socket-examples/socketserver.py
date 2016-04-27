#!/usr/bin/env python

import SocketServer
from threading import Thread

class EchoHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		#self.request is client details
		print "Connection come from: " + str(self.client_address)
		#self.request is client socket
		self.request.send("Hello client\n")
		data = 'data'
		while len(data):
			self.request.send("Input: ")
			data = self.request.recv(2048).strip()
			print "Client said: "+data
			self.request.send("Your input: "+data)
		print "Client out."
		self.request.close()

#Class thread
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass




#Running with no thread
"""server_address = ("0.0.0.0", 8000)
server = SocketServer.TCPServer(server_address, EchoHandler)"""

#Running with thread
server = ThreadedTCPServer(("0.0.0.0", 8000), EchoHandler)

server.serve_forever()

