class PiCameraUnthreadedStream():
    """ Rreads the PiCamera without threading.

    The PiVideoStream class within imutils.VideoStream provides a threaded way
    to read the PiCamera images. This class provides a way to read the PiCamera
    without threading, primarily intended for testing. For compatibility, the
    method names are the same as imutils.VideoStream.
    """
    def __init__(self, resolution=(320, 240), framerate=32, **kwargs):
        from picamera.array import PiRGBArray
        from picamera import PiCamera
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="bgr",
                                                     use_video_port=True)
        self.frame = None

    def read(self):
        f = next(self.stream)  # or f = self.stream.read()?
        self.frame = f.array
        self.rawCapture.truncate(0)
        return self.frame

    def stop(self):
        self.close()

    def close(self):
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
