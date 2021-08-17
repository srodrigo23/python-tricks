import cv2

def rescale_frame(frame_input, percent=50):
    width = int(frame_input.shape[1] * percent / 100)
    height = int(frame_input.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame_input, dim, interpolation=cv2.INTER_AREA)

#capture frames from a camera with device index=0
cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    rescaled_frame = rescale_frame(frame)
    (h, w) = rescaled_frame.shape[:2]
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    out = cv2.VideoWriter('output.avi', fourcc, 10, (w, h))
else:
    print("Camera is not opened")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        rescaled_frame = rescale_frame(frame)
        out.write(rescaled_frame)
        cv2.imshow("Output", rescaled_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# release the camera from video capture
cap.release()
out.release()
# De-allocate any associated memory usage
cv2.destroyAllWindows()