import socket 
import threading
import sys
import datetime        

class ClientThread(threading.Thread):
	def __init__(self,connect,address):
		threading.Thread.__init__(self)
		self.connectionSocket = connect
		self.addr = address


	def run(self):
		while True:
			request = connectionSocket.recv(1024).decode()
			
			print(request)
			headers = request.split('\n')
			filename = headers[0].split()[1]
			

			if filename == '/':
				filename = '/sucks.html'

			path = 'page'
			file = open(path + filename, 'rb')
			content = file.read()

			try:

				file = open(path + filename, 'rb')
				content = file.read()
				file.close()

				header = "HTTP/1.0 200 OK\n\n"


				#response = header.encode() + content


				header_info = {
					"Content-Length": len(content),
					"Keep-Alive": "timeout=%d,max=%d" %(10,100),
					"Connection": "Keep-Alive"
				}
				
				following_header = "\r\n".join("%s:%s" % (item, header_info[item]) for item in header_info)
				print (following_header)
				connectionSocket.sendall((header+ '\r\n'+following_header+ '\r\n\r\n').encode())
				connectionSocket.sendall(content)
			

				
			except FileNotFoundError:
				header = 'HTTP/1.0 404 Not Found\n\n'
				file_error= open(path +'file_error.html', 'rb')
				content = file_error.read()
				file_error.close()
				response = header.content() + content
				connectionSocket.sendall(response)
			


if __name__ == '__main__':
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	serverPort = 8080
	serverSocket.bind(('',serverPort))
	serverSocket.listen(5)
	threads = []

	while True:
		print('Listening on port %s ...' % serverPort)
		connectionSocket, addr = serverSocket.accept()
		print ("addr:\n", addr)
		client_thread = ClientThread(connectionSocket,addr)
		client_thread.setDaemon(True)
		client_thread.start()
		threads.append(client_thread)
	
	serverSocket.close()

