import socket
import sys
from socket import *

host = 'localhost'
serverPort = 6789

serverSocket = socket(AF_INET, SOCK_STREAM)                     #creating the server socket
serverSocket.bind((host, serverPort))                                   #binding the socket to port
serverSocket.listen(1)                                                     #waiting for the connection 
print('the web server is up on port: ', serverPort)

while True:
    print('Ready to serve....')
    connectionSocket, address = serverSocket.accept()               #accepting incoming client connection
    try:
        message = connectionSocket.recv(1024)                        #getting request message from client
        message.decode()
        filename = message.split()[1]                                    #getting file name from message
        print(filename)
        f = open(filename[1:])                                            #opening the file  
        outputdata = f.read()                                             #getting file content  
        connectionSocket.send('\nHTTP/1.1 200 OK\n\n'.encode())    #send one HTTP header line into socket
        for i in range(0, len(outputdata)):                               #send content of requested file to client  
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()                                          #closing client connection  
    except IOError:                                                       #send response message for FNF  
        connectionSocket.send('\nHTTP/1.1 404 Not Found\n\n'.encode())
        htmlErrorMessage = '<html><body><center><h3>Error 404: File Not Found</h3></center></body></html>'
        connectionSocket.send(htmlErrorMessage.encode())
        connectionSocket.close()                                          #closing client connection   

serverSocket.close()                                                      #closing server socket
sys.exit()                                                                   #terminate program after data is sent
