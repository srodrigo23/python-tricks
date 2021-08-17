from threading import Thread
import socket as s
import time

class Server():
    
    def __init__(self, host='', port=8485):
        self.host=host
        self.port=port
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.setup_server()
    
    def setup_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        
        self.cons = []
        self.setup_connections()
        # self.listen_messages()
    
    def setup_connections(self):
        thread = Thread(target=self.listen_connections, args=())
        thread.setDaemon(True)
        thread.start()
    
    def listen_connections(self):
        while True:
            conn, addr = self.socket.accept()
            self.cons.append((conn, addr))
            self.show_server_info()
    
    def show_server_info(self):
        print(f'Num. conections : { len(self.cons) }')
        for con in self.cons:
            print(f"Connection : {con[1][0]} Address : {con[1][1]}" )
        
Server()