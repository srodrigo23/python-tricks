import cv2, imutils, io, socket, struct, time, pickle
import numpy as np

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('127.0.0.1', 8485))

abs_source = '/Users/sergiorodrigo/Documents/tesis/test/media/video5.mp4'
cam = cv2.VideoCapture(abs_source)
img_counter = 0
time.sleep(2.0)

# to encode jpeg image format
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    if ret:
        frame = imutils.resize(frame, width=320)
        frame = cv2.flip(frame, 180)

        result, image = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(image, 0)
        size = len(data)

        if img_counter%10==0:
            client_socket.sendall(struct.pack(">L", size) + data)
            cv2.imshow('client',frame)
        img_counter += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()