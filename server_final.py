import socket
import datetime
import threading


class ClientThread(threading.Thread):
	def __init__(self, connect, address):
		threading.Thread.__init__(self)
		self.connectionSocket = connect
		self.addr = address
	def run(self):
		while True:
			try:
				request = connectionSocket.recv(1024).decode()
				if not request:
					break
				print (request)
				headers = request.split('\n')
				filename = headers[0].split()[1]

				if filename == '/':
					filename = 'sucks.html'

				file = open('page/'+ filename, 'rb')
				outputdata = file.read()
				now = datetime.datetime.now()
				first_header = "HTTP/1.1 200 OK"
				header_info = {
					"Date": now.strftime("%Y-%m-%d %H:%M"),
					"Content-Length": len(outputdata),
					"Keep-Alive": "timeout=%d,max=%d" %(10,100),
					"Connection": "Keep-Alive"
					
				}
				following_header = "\r\n".join("%s:%s" % (item, header_info[item]) for item in header_info)
				print ("following_header:", following_header)
				connectionSocket.sendall((first_header +'\r\n'+following_header + '\r\n\r\n').encode())
				connectionSocket.sendall(outputdata)



			except FileNotFoundError:

				first_header = 'HTTP/1.0 404 Not Found'
				file_error= open('page/file_error.html','rb')
				content = file_error.read()
				file_error.close()
				header_info = {
					"Date": now.strftime("%Y-%m-%d %H:%M"),
					"Content-Length": len(content),
					"Keep-Alive": "timeout=%d,max=%d" %(10,100),
					"Connection": "Keep-Alive"
					
				}
				following_header = "\r\n".join("%s:%s" % (item, header_info[item]) for item in header_info)
				print ("following_header:", following_header)
				connectionSocket.sendall((first_header +'\r\n'+following_header + '\r\n\r\n').encode())
				connectionSocket.sendall(content)
				
				


if __name__ == '__main__':
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)	
	serverPort = 8080
	serverSocket.bind(('',serverPort))
	serverSocket.listen(5)
	threads=[]

	while True:
		
		print ('Ready to serve...')
		connectionSocket, addr = serverSocket.accept()
		print ("addr:\n", addr)
		
		client_thread = ClientThread(connectionSocket,addr)
		client_thread.setDaemon(True)
		client_thread.start()
		threads.append(client_thread)

	serverSocket.close()
