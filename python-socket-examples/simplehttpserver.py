import SocketServer
import SimpleHTTPServer

class HttpRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/admin":
			self.wfile.write("Only for admin.\n")
			self.wfile.write(self.headers)
		else:
			SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

httpServer = SocketServer.TCPServer(("", 10000), HttpRequestHandler)

httpServer.serve_forever()