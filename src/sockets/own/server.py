from threading import Thread
import socket as s
import time

class Server():
    
    def __init__(self, host='', port=8485):
        self.host=host
        self.port=port
        self.setup_server()
    
    def setup_server(self):
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(10)
        except socket.error as e:
            print(str(e))
        self.cons = [] # to manage conections
        self.listen_connections()
    
    def start_new_connection(self, connection):
        thread = Thread(target=self.listen_connections, args=(connection))
        thread.setDaemon(True)
        thread.start()
    
    def run_connection(self, connection):
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
    
    def listen_connections(self):
        print("Listen connections >")
        while True:
            conn, addr = self.socket.accept()
            self.cons.append((conn, addr))    
            self.show_server_info()
    
    def show_server_info(self):
        print(f'Num. conections : { len(self.cons) }')
        for con in self.cons:
            print(f"Connection : {con[1][0]} Address : {con[1][1]}" )
Server()