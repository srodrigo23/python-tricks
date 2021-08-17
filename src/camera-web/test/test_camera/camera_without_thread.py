import cv2
import imutils
import numpy as np

from imutils.video import FPS

video = cv2.VideoCapture(0)
fps = FPS().start()

while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break
    frame = imutils.resize(frame, width=450)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    fps.update()

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
video.release()
cv2.destroyAllWindows()