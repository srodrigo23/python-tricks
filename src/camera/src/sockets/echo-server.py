#!/usr/bin/env python3

import socket
host = '127.0.0.1' # localhost
port = 65432       # port to listen non privileged ports are > 1023

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            print('Received from client', data)
