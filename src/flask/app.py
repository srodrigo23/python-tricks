from flask import Flask, render_template, Response
import cv2

#initialize the flask app
app = Flask(__name__)
camera = cv2.VideoCapture(0)

def genFrames():
    while True:
        success, frame = camera.read() # read the camera Frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') #concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(genFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(port=5000, debug=True)