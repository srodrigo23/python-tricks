import socket
# import uuid

class Client():
    
    def __init__(self, id, host='127.0.0.1', port=1233):
        # self.id = uuid.uuid1().int
        self.id = id
        self.socket = socket.socket()
        self.host=host
        self.port=port
        self.connect_server()
        self.run_listen_messages()
    
    def connect_server(self):
        print('Looking for a connection...')
        try:
            self.socket.connect((self.host, self.port))
        except socket.error as e:
            print(str(e))
        
        serv_ans = self.socket.recv(1024)
        print(serv_ans.decode('utf-8'))
    
    def start_send_thread(self):
        thread = Thread(target=self.run_connection, args=(conn, ))
        thread.setDaemon(True)
        thread.start()
    
    # def run_send_messages(self):
        

    def run_listen_messages(self):
        while True:    
            inp = input(f'Client { self.id } > ')
            self.socket.send(str.encode(inp))
            #Waiting answer
            answer = self.socket.recv(1024)
            print(answer.decode('utf-8'))

Client(id=1)