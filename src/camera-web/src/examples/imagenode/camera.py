""" 
Methods and attributes of a camera

Each camera is setup and started using the settings in the yaml file.
Includes setup of detectors, e.g., detector for motion

Parameters:
    camera (text): dict key of current camera being instantiated
    cameras (dict): dictionary of all cameras named in YAML file
    settings (Settings object): settings object created from YAML file
"""

class Camera():
    
    def __init__(self, camera, cameras, settings):
        """ Initializes all the camera settings from settings in the YAML file.
        """
        self.cam = None
        self.jpeg_quality = 95  # 0 to 100, higher is better quality, 95 is cv2 default
        # check picamera version
        try:
            picamversion = require('picamera')[0].version
        except:
            picamversion = '0'

        if 'threaded_read' in cameras[camera]:  # threaded on non-threaded camera reading
            self.threaded_read = cameras[camera]['threaded_read']
        else:
            self.threaded_read = True
        if 'resolution' in cameras[camera]:
            self.resolution = literal_eval(cameras[camera]['resolution'])
        else:
            self.resolution = (320, 240)
        if 'framerate' in cameras[camera]:
            self.framerate = cameras[camera]['framerate']
        else:
            self.framerate = 32
        if 'vflip' in cameras[camera]:
            self.vflip = cameras[camera]['vflip']
        else:
            self.vflip = False
        if 'resize_width' in cameras[camera]:
            # resize_width is a percentage value
            # width in pixels will be computed later after reading a test image
            self.resize_width = cameras[camera]['resize_width']
        else:
            self.resize_width = None
        if 'viewname' in cameras[camera]:
            self.viewname = cameras[camera]['viewname']
        else:
            self.viewname = ' '
        if 'src' in cameras[camera]:
            self.src = cameras[camera]['src']
        else:
            self.src = 0
        if 'exposure_mode' in cameras[camera]:
            self.exposure_mode = cameras[camera]['exposure_mode']
        else:
            self.exposure_mode = None
        if 'iso' in cameras[camera]:
            self.iso = cameras[camera]['iso']
        else:
            self.iso = 0  # default value
        if 'shutter_speed' in cameras[camera]:
            self.shutter_speed = cameras[camera]['shutter_speed']
        else:
            self.shutter_speed = 0  # default value
        if 'sharpness' in cameras[camera]:
            self.sharpness = cameras[camera]['sharpness']
        else:
            self.sharpness = 0  # default value
        if 'contrast' in cameras[camera]:
            self.contrast = cameras[camera]['contrast']
        else:
            self.contrast = 0  # default value
        if 'brightness' in cameras[camera]:
            self.brightness = cameras[camera]['brightness']
        else:
            self.brightness = 50  # default value
        if 'exposure_compensation' in cameras[camera]:
            self.exposure_compensation = cameras[camera]['exposure_compensation']
        else:
            self.exposure_compensation = 0  # 0 default value, integer value between -25 and 25
        if 'awb_mode' in cameras[camera]:
            self.awb_mode = cameras[camera]['awb_mode']
        else:
            self.awb_mode = 'auto'  # default value

        self.detectors = []
        if 'detectors' in cameras[camera]:  # is there at least one detector
            self.setup_detectors(cameras[camera]['detectors'],
                                 settings.nodename,
                                 self.viewname)
        if camera[0].lower() == 'p':  # this is a picam
            # start PiCamera and warm up; inherits methods from
            # imutils.VideoStream unless threaded_read is False; then uses class
            # PiCameraUnthreadedStream to read the PiCamera in an unthreaded way
            if self.threaded_read:
                self.cam = VideoStream(usePiCamera=True,
                                       resolution=self.resolution,
                                       framerate=self.framerate).start()
            else:
                self.cam = PiCameraUnthreadedStream(resolution=self.resolution,
                                                    framerate=self.framerate)

            # if an exposure mode has been set in yaml, set it
            if self.exposure_mode:
                self.cam.camera.exposure_mode = self.exposure_mode
            # if an iso has been set in yaml, set it
            if self.iso:
                self.cam.camera.iso = self.iso
            # if an iso has been set in yaml, set it
            if self.shutter_speed:
                self.cam.camera.shutter_speed = self.shutter_speed
            # if an sharpness has been set in yaml, set it
            if self.sharpness:
                self.cam.camera.sharpness = self.sharpness
            # if an contrast has been set in yaml, set it
            if self.contrast:
                self.cam.camera.contrast = self.contrast
            # if an brightness has been set in yaml, set it
            if self.brightness:
                self.cam.camera.brightness = self.brightness
            # if an exposure_compensation has been set in yaml, set it
            if self.exposure_compensation:
                self.cam.camera.exposure_compensation = self.exposure_compensation
            # if an awb_mode has been set in yaml, set it
            if self.awb_mode:
                self.cam.camera.awb_mode = self.awb_mode
            self.cam_type = 'PiCamera'
        else:  # this is a webcam (not a picam)
            self.cam = VideoStream(src=0).start()
            self.cam_type = 'webcam'
        sleep(3.0)  # allow camera sensor to warm up

        # self.text is the text label for images from this camera.
        # Each image that is sent is sent with a text label so the hub can
        # file them by nodename, viewname, and send_type
        # example: JeffOffice Window|jpg
        # Nodename and View name are in one field, separated by a space.
        # send_type is in the next field
        # The 2 field names are separaged by the | character
        node_and_view = ' '.join([settings.nodename, self.viewname]).strip()
        self.text = '|'.join([node_and_view, settings.send_type])

        # set up camera image queue
        self.cam_q = deque(maxlen=settings.queuemax)

    def setup_detectors(self, detectors, nodename, viewname):
        """ Create a list of detectors for this camera

        Parameters:
            detectors (dict): detectors for this camera from YAML file
            nodename (str): nodename to identify event messages and images sent
            viewnane (str): viewname to identify event messages and images sent
        """

        if isinstance(detectors, list):
            for lst in detectors:
                for detector in lst:
                    det = Detector(detector, lst, nodename, viewname)  # create a Detector instance
                    self.detectors.append(det)  # add to list of detectors for this camera
        else:
            for detector in detectors:  # for each camera listed in yaml file
                det = Detector(detector, detectors, nodename, viewname)  # create a Detector instance
                self.detectors.append(det)  # add to list of detectors for this camera
