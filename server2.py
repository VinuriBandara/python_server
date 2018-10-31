import socket
import sys



def handle_request(request):

    headers = request.split('\n')
    filename = headers[0].split()[1]
    if filename == '/':
        filename = '/sucks.html'

    try:
        header = 'HTTP/1.0 200 OK\n\n'


        fin = open('htdocs/page' + filename)
        content = fin.read()
        fin.close()

        # if (filename.endswith(".jpg")):
        #     mimetype ='image/jpg'
        # elif(filename.endswith(".css")):
        #     mimetype = 'text/css'
        # else:
        #     mimetype = 'text/html'

        # header += 'Content-Type: '+str(mimetype)+'\n\n'



        #response = 'HTTP/1.0 200 OK\n\n' + content 

    except FileNotFoundError:
        header = 'HTTP/1.0 404 Not Found\n\n'
        file_error= open('htdocs/page/file_error.html')
        content = file_error.read()
        file_error.close()

              
    response = header
    response += content
    return response



SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    
    client_connection, client_address = server_socket.accept()

   
    request = client_connection.recv(1024).decode()
    response= handle_request(request)
    print(request)
    
    client_connection.sendall(response.encode())

   
    client_connection.close()


server_socket.close()
