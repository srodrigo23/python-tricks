import time
import zmq

context =  zmq.Context()

socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    # wait for next request from client
    message = socket.recv()
    print(f"Recieved request: {message}")

    # Do some work
    time.sleep(0.2)

    # Send reply back to client
    socket.send(b"World")