import socket
import sys

try:
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    print ("Socket successfully created")
except socket.error as error:
    print("Socket creation has failed with error %s" % error)
    
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#print ("Socket successfully created")

port = 8888             

s.bind(('', port))

print ("socket binded to %s" %(port))


s.listen(5)     
print ("socket is listening")      

while True:

   c, addr = s.accept()
   print ('Got connection from', addr)
   request = c.recv(1024).decode()
   print (request)
   c.sendall('Thank you for connecting to my server'.encode())
   c.close()        
