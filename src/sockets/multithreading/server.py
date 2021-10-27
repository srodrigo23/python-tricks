import socket
import os
from _thread import start_new_thread

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0

#where is this example?
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection')

ServerSocket.listen(1)

def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server'))
    while True:
        data = connection.recv(2048)
        entry = data.decode('utf-8') 
        print(entry)
        reply = 'Server says ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (client, ))
    print(get_ident())
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))