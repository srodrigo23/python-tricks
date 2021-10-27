import socketserver
import threading

ServerAddress = ("127.0.0.1", 6060)

class MyTCPClientHandler(socketserver.StreamRequestHandler):

    def handle(self):
        # Receive and print the data received from client
        print("Recieved one request from {}".format(self.client_address[0]))
        msg = self.rfile.readline().strip()
        print("Data Recieved from client is:".format(msg))
        print(msg)  
        print("Thread Name:{}".format(threading.current_thread().name))
        
# Create a Server Instance
TCPServerInstance = socketserver.ThreadingTCPServer(ServerAddress, MyTCPClientHandler)
TCPServerInstance.serve_forever()# Make the server wait forever serving connections