import socket
import threading
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

	@staticmethod
	def unpack_http_header(header) :
		element_line = header.rstrip('\r\n\r\n').split('\r\n')
		first_method = element_line[0]
		result = dict()
		for one in element_line[1:]:
			key, value = one.split(': ', 1)
			value = value.lstrip()
			result[key] = value
		print result
		return first_method, result

	def receive_http_request(self):
		packet = ''
		while True :
			packet += self.request.recv(1) #from client
			if '\r\n\r\n' in packet:
				break

	def receive_http_response_header(self, s):
		packet = ''
		while True :
			packet += s.recv(1)
			if '\r\n\r\n' in packet:
				break
		return packet

	def handle(self):
		data = self.receive_http_request(1024)
		f, request_header = unpack_http_header(data)
		print f

		host = request_header['Host']
		port = 80

		s = socket(AF_INET, SOCK_STREAM)
		s.connect((host,80))
		s.send('GET / HTTP/1.1\r\nHost: gilgil.net\r\nConnection: keep-alive\r\n\r\n')

		#send dummy request and receive
		request_result, response_header = unpack_http_header(receive_http_response_header(s))
		print request_result

		if (response_header.get('Connection', '') == 'close') :
			s.close()
			s = socket(AF_INET, SOCK_STREAM)
			s.connect((host,80))


		# send real request
		s.send('\r\n\r\n' + data)

		#receive real response
		#self.receive_response(s)

	def finish(self):
		pass

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == "__main__":
	SocketServer.TCPServer.allow_reuse_address = True
	HOST, PORT = "localhost", 7777
	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	server.serve_forever()