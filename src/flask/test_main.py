from flask import Flask, render_template, Response
from image_hub import ImageHub

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(hub):
    while True:
        msg, frame = hub.recv_jpg()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        hub.send_reply(b'OK')

@app.route('/video')
def video():
    return Response(gen(ImageHub()), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Main execution 
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    
    