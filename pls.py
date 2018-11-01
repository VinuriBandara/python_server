#import socket module
__author__ = 'Xi Su'

import socket
import datetime
import threading

"""
memo:
"thread" vs "threading" : thread module has been considered as "deprecated" in python3, thread is _thread;
"thread" is infrastructure code for threding to implement.
Using threading.Thread the object to pass the paramenter and Thread.start(); for loop to join Thread
Override the Thread object __init__ and run methods
In each thread, do not put connectionSocket.close()in thread while loop.

"""
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
					# "Date": now.strftime("%Y-%m-%d %H:%M"),
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
					# "Date": now.strftime("%Y-%m-%d %H:%M"),
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
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)#Prepare a sever socket
	#Fill in start
	serverPort = 8080
	serverSocket.bind(('',serverPort))
	serverSocket.listen(5)
	threads=[]
	#Fill in end
	while True:
		#Establish the connection
		print ('Ready to serve...')
		connectionSocket, addr = serverSocket.accept()
		print ("addr:\n", addr)
		#Fill in start
		#Fill in end
		client_thread = ClientThread(connectionSocket,addr)
		client_thread.setDaemon(True)
		client_thread.start()
		threads.append(client_thread)

	#main thread wait all threads finish then close the connection
	"""
	# for thread in threads:
	# 	thread.join()
	If I put this, Chrome will not gonna work, safari will work.
	"""
	serverSocket.close()
