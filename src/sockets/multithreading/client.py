import socket
import time

# Client to 
# https://instructobit.com/tutorial/101/Reconnect-a-Python-socket-after-it-has-lost-its-connection

ClientSocket = None 
host='127.0.0.1'
port=1233

def connect():    
    print('Waiting for connection')
    global ClientSocket
    while True:
        try:
            ClientSocket = socket.socket()
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))
            print('Attempting again')
            time.sleep(2)
        else:
            print('connected')
            break

connect()
Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))

while True:
    Input = input('Say something : ')
    try:
        ClientSocket.send(str.encode(Input))
    except socket.error as e:
        print(str(e))
        connect()
                
    try:
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
    except socket.error as e:
        print(str(e))
        connect()