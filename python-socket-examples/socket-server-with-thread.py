import threading
import socket

HOST = '0.0.0.0'
PORT = 8888

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socket.bind((HOST, PORT))
socket.listen(1)

def echo(client):
	client.send("Input: ")
	while True:
		data = client.recv(2048)
		print "Client sent: " + data
		client.send("You said: " + data)

if __name__ == "__main__":
	print "Waiting client..."
	while True:
		(client, (client_ip, client_port)) = socket.accept()
		print "Connection from %s:%d" % (client_ip, client_port)
		thread = threading.Thread(target=echo, args=(client, ))
		thread.start()

	print "Closing connection..."
	client.close()

	print "Server close..."
	socket.close()