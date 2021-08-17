
import numpy as np
import cv2
import time
#we load video
camera = cv2.VideoCapture(0)
#we initialize the first frame to empty
#it will help to obtain the fund
background = None
#We go throught all the frames
while True:
    grabbed, frame = camera.read()
    #If we have reached the end of the video we leave
    if not grabbed:
        break
    # we convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # we apply smothing to remove noise
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # If we have not yet obtained the fund, we obtain it
    # It will be the first frame we get
    if background is None:
        background = gray
        continue
    #calculation if the difference betwen the background
    # and the current frame
    subtraction = cv2.absdiff(background, gray)
    #we apply a threshold
    threshold = cv2.threshold(subtraction, 30, 255, cv2.THRESH_BINARY) [1]
    # We expand the threshold to cover holes
    threshold = cv2.dilate(threshold, None, iterations=2)
    # We copy the threshold to detect the contours
    contourimg = threshold.copy()

    # We look for contour in the image
    outlines, _ = cv2.findContours(contourimg, 
            cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    # We go through all the contours in the image
    for c in outlines:
        # We remove the smallest contours
        if cv2.contourArea(c) < 10000 :
            continue

        # We obtain the bounds of the contour, the largest
        # rectangle that encompasses the contour
        (x, y, w, h) = cv2.boundingRect(c)
        # We draw the rectangle of the bounds
        cv2.rectangle(frame, (x, y), (x+ w, y + h), (0, 255, 0), 1)

    # We show the images of the camera, the threshold and the subtraction
    cv2.imshow("Camera",       frame)
    cv2.imshow("Threshold",    threshold)
    cv2.imshow("Substraction", subtraction)
    cv2.imshow("Contour",      contourimg)

    #we capture a key to exit
    key = cv2.waitKey(1) & 0xFF
    #Timeout for it to look good
    time.sleep(1000)

    # If you have pressed the letter s, we exit
    if key == ord('s'):
        break

    # We release the camera and close all the windows
    camera.release()
    cv2.destroyAllWindows()