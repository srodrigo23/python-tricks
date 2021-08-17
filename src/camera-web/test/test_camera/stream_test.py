import numpy as np
import time
import cv2

from camera_stream import CameraStream
from imutils.video import FPS

stream = CameraStream(0).start()
fps = FPS().start()

time.sleep(1.0) # to prepare camera
#TODO: resize image
while True:#stream.is_more():
    frame = stream.read()    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])
    # display the size of the queue on the frame
    cv2.putText(frame, "Queue Size: {}".format(stream.my_queue.qsize()),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)	
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    fps.update()

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cv2.destroyAllWindows()
stream.stop()