
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera

import time
import cv2
import imutils

camera = PiCamera()
camera.resolution = (321, 240)
camera.framerate = 32

rawCapture = PiRGBArray(camera, size=(320, 240))
stream = camera.capture_continuous(rawCapture, 
                                 format="bgr",
                                use_video_port=True)
print("[INFO] sampling frames from `picamera` module...")
time.sleep(2.0)

fps=FPS().start()

for (i,f) in enumerate(stream):
    frame=f.array
    frame=imutils.resize(frame, width=400)
    
    cv2.imshow("Frame", frame)
    
    rawCapture.capture(0)
    fps.update()
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
stream.close()
rawCapture.close()
camera.close()