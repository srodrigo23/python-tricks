import socket
import time
from imutils.video import VideoStream
import imagezmq

sender = imagezmq.ImageSender(connect_to='tcp://192.168.43.98:5555')

rpi_name = socket.gethostname() #send RPi hostname wiht each image
picam = VideoStream(usePiCamera=False).start()
# time.sleep(2.0) # allow camera sensor to warm up
while True:
    image = picam.read()
    sender.send_image(rpi_name, image)
