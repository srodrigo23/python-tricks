import os
import sys
import yaml
import pprint
import signal
import logging
import itertools
import threading
import multiprocessing

from time import sleep
from datetime import datetime
from ast import literal_eval
from collections import deque

import numpy as np
import cv2
import imutils

from imutils.video import VideoStream

import zmq  # needed to use zmq.LINGER in ImageNode.closall methods
import imagezmq

from tools.utils import interval_timer
from tools.nodehealth import HealthMonitor
from tools.utils import versionCompare
from pkg_resources import require

class ImageNode:

    def __init__(self, settings):
        # set various node attributes; also check that numpy and OpenCV are OK
        self.tiny_image = np.zeros((3, 3), dtype="uint8")  # tiny blank image
        ret_code, jpg_buffer = cv2.imencode(".jpg", self.tiny_image, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        self.tiny_jpg = jpg_buffer  # matching tiny blank jpeg
        self.jpeg_quality = 95
        self.pid = os.getpid()  # get process ID of this program

        # open ZMQ link to imagehub
        self.sender = imagezmq.ImageSender(connect_to=settings.hub_address)
        self.sender.zmq_socket.setsockopt(zmq.LINGER, 0)  # prevents ZMQ hang on exit

        # If settings.REP_watcher is True, pick the send_frame function
        #  that does time recording of each REQ and REP. Start REP_watcher
        #  thread. Set up deques to track REQ and REP times.
        self.patience = settings.patience  # how long to wait in seconds
        if settings.send_type == 'image':  # set send function to image
            if settings.REP_watcher:
                self.send_frame = self.send_image_frame_REP_watcher
            else:
                self.send_frame = self.send_image_frame
        else: # anything not spelled 'image' sets send function to jpg
            if settings.REP_watcher:
                self.send_frame = self.send_jpg_frame_REP_watcher
            else:
                self.send_frame = self.send_jpg_frame
        if settings.REP_watcher:  # set up deques & start thread to watch for REP
            threading.Thread(daemon=True, target=self.REP_watcher).start()
            self.REQ_sent_time = deque(maxlen=1)
            self.REP_recd_time = deque(maxlen=1)

        # set up message queue to hold (text, image) messages to be sent to hub
        if settings.send_threading:  # use a threaded send_q sender instead
            self.send_q = SendQueue(maxlen=settings.queuemax,
                                    send_frame=self.send_frame,
                                    process_hub_reply=self.process_hub_reply)
            self.send_q.start()
        else:
            self.send_q = deque(maxlen=settings.queuemax)

        # start system health monitoring & get system type (RPi vs Mac etc)
        self.health = HealthMonitor(settings, self.send_q)

        self.sensors = []  # need an empty list even if no sensors
        self.lights = []
        if self.health.sys_type == 'RPi':  # set up GPIO & sensors
            if settings.sensors or settings.lights:
                global GPIO
                import RPi.GPIO as GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)
            if settings.sensors:   # is there at least one sensor in yaml file
                self.setup_sensors(settings)
            if settings.lights:   # is there at least one light in yaml file
                self.setup_lights(settings)

        # set up and start camera(s)
        self.camlist = []  # need an empty list if there are no cameras
        if settings.cameras:  # is there at least one camera in yaml file
            self.setup_cameras(settings)

        # Read a test image from each camera to check and verify:
        # 1. test that all cameras can successfully read an image
        # 2. determine actual camera resolution from returned image size
        # 3. if resize_width has been set, test that it works without error
        # 4. for each detector, convert roi_pct to roi_pixels
        # Note that image size returned from reading the camera can vary from
        # requested resolution size, especially in webcams
        for camera in self.camlist:
            testimage = camera.cam.read()
            image_size = testimage.shape  # actual image_size from this camera
            width, height = image_size[1], image_size[0]
            camera.res_actual = (width, height)
            if camera.resize_width:
                camera.width_pixels = (width * camera.resize_width) // 100
                testimage = imutils.resize(testimage, width=camera.width_pixels)
                image_size = testimage.shape
                width, height = image_size[1], image_size[0]
            else:
                camera.width_pixels = width
            camera.res_resized = (width, height)
            # compute ROI in pixels using roi_pct and current image size
            for detector in camera.detectors:
                top_left_x = detector.roi_pct[0][0] * width // 100
                top_left_y = detector.roi_pct[0][1] * height // 100
                bottom_right_x = detector.roi_pct[1][0] * width // 100
                bottom_right_y = detector.roi_pct[1][1] * height // 100
                detector.top_left = (top_left_x, top_left_y)
                detector.bottom_right = (bottom_right_x, bottom_right_y)
                detector.roi_pixels = (detector.top_left, detector.bottom_right)
                detector.roi_area = ((bottom_right_x - top_left_x)
                                     * (bottom_right_y - top_left_y))
                if detector.detector_type == 'motion':
                    detector.min_area_pixels = (detector.roi_area
                                                * detector.min_area) // 100
                # location of timestamp based on image size
                if detector.draw_time:
                    time_x = detector.draw_time_org[0] * width // 100
                    time_y = detector.draw_time_org[1] * height // 100
                    detector.draw_time_org = (time_x, time_y)

        if settings.print_node:
            self.print_node_details(settings)

        # send an imagenode startup event message with system values
        text = '|'.join([settings.nodename,
                        'Restart',
                        self.health.hostname,
                        self.health.sys_type,
                        self.health.ipaddress,
                        self.health.ram_size,
                        self.health.time_since_restart])
        text_and_image = (text, self.tiny_image)
        self.send_q.append(text_and_image)

    def print_node_details(self, settings):
        print('Node details after setup and camera test read:')
        print('  Node name:', settings.nodename)
        print('  System Type:', self.health.sys_type)
        for cam in self.camlist:
            print('  Camera:', cam.cam_type)
            print('    Resolution requested:', cam.resolution)
            print('    Resolution actual after cam read:', cam.res_actual)
            print('    Resize_width setting:', cam.resize_width)
            print('    Resolution after resizing:', cam.res_resized)
            if cam.cam_type == 'PiCamera':
                # check picamera version
                try:
                    picamversion = require('picamera')[0].version
                except:
                    picamversion = '0'
                print('    PiCamera:')
                # awb_mode: off, auto, sunlight, cloudy, shade, tungsten, fluorescent, incandescent, flash, horizon
                print('        awb_mode:', cam.cam.camera.awb_mode, '(default = auto)')
                print('        brightness:', cam.cam.camera.brightness, '(default = 50, integer between 0 and 100)')
                print('        contrast:', cam.cam.camera.contrast, '(default = 0, integer between -100 and 100)')
                # exposure_compensation: integer value between -25 and 25
                print('        exposure_compensation:', cam.cam.camera.exposure_compensation, '(default = 0)')
                # exposure_mode:  - off, auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong,
                #                   fixedfps, antishake, fireworks
                print('        exposure_mode:', cam.cam.camera.exposure_mode, '(default = auto)')
                print('        framerate:', cam.cam.camera.framerate, '(default = 30)')
                print('        iso:', cam.cam.camera.iso, '(default = 0 for auto - 0,100,200,320,400,500,640,800)')
                # meter_mode:  average, spot, backlit, matrix
                print('        meter_mode:', cam.cam.camera.meter_mode, '(default = average)')
                print('        saturation:', cam.cam.camera.saturation, '(default = 0, integer between -100 and 100)')
                print('        sharpness:', cam.cam.camera.sharpness, '(default = 0, integer between -100 and 100)')
                print('        shutter_speed:', cam.cam.camera.shutter_speed, '(microseconds - default = 0 for auto)')
                if versionCompare('1.6', picamversion) != 1:
                    print('        analog_gain:', float(cam.cam.camera.analog_gain), '(read-only)')
                    # awb_gains: typical values for the gains are between 0.9 and 1.9 - when awb_mode = off
                    print('        awb_gains:', cam.cam.camera.awb_gains)
                    print('        digital_gain:', float(cam.cam.camera.digital_gain), '(read-only)')
                    print('        exposure_speed:', cam.cam.camera.exposure_speed, '(microseconds - read-only)')
                if versionCompare('1.13', picamversion) != 1:
                    print('        revision:', cam.cam.camera.revision, '(ov5647 = V1, imx219 = V2, imx477 = HQ)')

            for detector in cam.detectors:
                print('    Detector:', detector.detector_type)
                print('      ROI:', detector.roi_pct, '(in percents)')
                print('      ROI:', detector.roi_pixels, '(in pixels)')
                print('      ROI area:', detector.roi_area, '(in pixels)')
                print('      ROI name:', detector.roi_name)
                print('      send_test_images:', detector.send_test_images)
                print('      send_count:', detector.send_count)
                if detector.detector_type == 'light':
                    print('      threshold:', detector.threshold)
                    print('      min_frames:', detector.min_frames)
                elif detector.detector_type == 'motion':
                    print('      delta_threshold:', detector.delta_threshold)
                    print('      min_motion_frames:', detector.min_motion_frames)
                    print('      min_still_frames:', detector.min_still_frames)
                    print('      min_area:', detector.min_area, '(in percent)')
                    print('      min_area:', detector.min_area_pixels, '(in pixels)')
                    print('      blur_kernel_size:', detector.blur_kernel_size)
                    print('      print_still_frames:', detector.print_still_frames)
        print()

    def setup_sensors(self, settings):
        """ Create a list of sensors from the sensors section of the yaml file

        Typical sensors include temperature and humidity, but PIR motion
        detectors, light meters and other are possible

        Parameters:
            settings (Settings object): settings object created from YAML file
        """

        for sensor in settings.sensors:  # for each sensor listed in yaml file
            s = Sensor(sensor, settings.sensors, settings, self.tiny_image,
                       self.send_q)
            self.sensors.append(s)  # add it to the list of sensors

    def setup_lights(self, settings):
        """ Create a list of lights from the lights section of the yaml file

        Lights are controlled by the RPI GPIO pins. The light settings name
        each light and assign it a GPIO pin

        Parameters:
            settings (Settings object): settings object created from YAML file
        """

        for light in settings.lights:  # for each light listed in yaml file
            lst = Light(light, settings.lights, settings)  # create a Light instance with settings
            self.lights.append(lst)  # add it to the list of lights

    def setup_cameras(self, settings):
        """ Create a list of cameras from the cameras section of the yaml file

        Often, the list will contain a single PiCamera, but it could be a
        PiCamera with one or more webcams. Or one or more webcams with no
        PiCamera.

        Parameters:
            settings (Settings object): settings object created from YAML file
        """
        for camera in settings.cameras:  # for each camera listed in yaml file
            cam = Camera(camera, settings.cameras, settings)  # create a Camera instance
            self.camlist.append(cam)  # add it to the list of cameras

    def REP_watcher(self):
        """ checks that a REP was received after a REQ; fix_comm_link() if not

        When running in production, watching for a stalled ZMQ channel is required.
        The REP_watcher yaml option enables checking that REP is received after REQ.

        Runs in a thread; both REQ_sent_time & REP_recd_time are deque(maxlen=1).
        Although REPs and REQs can be filling the deques continuously in the main
        thread, we only need to occasionally check recent REQ / REP times. When
        we have not received a timely REP after a REQ, we have a broken ZMQ
        communications channel and call self.fix_comm_link().

        """
        while True:
            sleep(self.patience)  # how often to check
            try:
                recent_REQ_sent_time = self.REQ_sent_time.popleft()
                # if we got here; we have a recent_REQ_sent_time
                sleep(1.0)  # allow time for receipt of a REP
                try:
                    recent_REP_recd_time = self.REP_recd_time.popleft()
                except IndexError:  # there was a REQ, but no REP was received
                    self.fix_comm_link()
                # if we got here; we have a recent_REP_recd_time
                interval = recent_REP_recd_time - recent_REQ_sent_time
                if  interval.total_seconds() <= 0.0:
                    # recent_REP_recd_time is not later than recent_REQ_sent_time
                    self.fix_comm_link()
            except IndexError: # there wasn't a time in REQ_sent_time
                # so there is no REP expected,
                # ... so continue to loop until there is a time in REQ_sent_time
                pass

    def send_jpg_frame(self, text, image):
        """ Compresses image as jpg before sending

        Function self.send_frame() is set to this function if jpg option chosen
        """

        ret_code, jpg_buffer = cv2.imencode(".jpg", image,
                                            [int(cv2.IMWRITE_JPEG_QUALITY),
                                             self.jpeg_quality])
        hub_reply = self.sender.send_jpg(text, jpg_buffer)
        return hub_reply

    def send_image_frame(self, text, image):
        """ Sends image as unchanged OpenCV image; no compression

        Function self.send_frame() is set to this function if image option chosen
        """

        hub_reply = self.sender.send_image(text, image)
        return hub_reply


    def send_jpg_frame_REP_watcher(self, text, image):
        """ Compresses image as jpg before sending; sends with RPI_watcher deques

        Function self.send_frame() is set to this function if jpg option chosen
        and if REP_watcher option is True. For each (text, jpg_buffer) that is
        sent, the current time is appended to a deque before and after the send.
        This allows comparing times to check if a REP has been received after
        the (text, jpg_buffer) REQ has been set. See self.REP_watcher() method
        for details.
        """

        ret_code, jpg_buffer = cv2.imencode(
            ".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY),
            self.jpeg_quality])
        self.REQ_sent_time.append(datetime.utcnow())  # utcnow 2x faster than now
        try:
            hub_reply = self.sender.send_jpg(text, jpg_buffer)
        except:  # add more specific exception, e.g. ZMQError, after testing
            print("Exception at sender.send_jpg in REP_watcher function.")
            self. fix_comm_link()
        self.REP_recd_time.append(datetime.utcnow())
        return hub_reply

    def send_image_frame_REP_watcher(self, text, image):
        """ Sends uncompressed OpenCV image; sends with RPI_watcher deques

        Function self.send_frame() is set to this function if image option chosen
        and if REP_watcher option is True. For each (text, jpg_buffer) that is
        sent, the current time is appended to a deque before and after the send.
        This allows comparing times to check if a REP has been received after
        the (text, jpg_buffer) REQ has been set. See self.REP_watcher() method
        for details.
        """

        self.REQ_sent_time.append(datetime.utcnow())  # utcnow 2x faster than now
        try:
            hub_reply = self.sender.send_image(text, image)
        except:  # add more specific exception, e.g. ZMQError, after testing
            print("Exception at sender.send_image in REP_watcher function.")
            self. fix_comm_link()
        self.REP_recd_time.append(datetime.utcnow())
        return hub_reply

    def read_cameras(self):
        """ Read one image from each camera and run detectors.

        Perform vflip and image resizing if requested in YAML setttings file.
        Append transformed image to cam_q queue.
        """
        for camera in self.camlist:
            image = camera.cam.read()
            if camera.vflip:
                image = cv2.flip(image, -1)
            if camera.resize_width:
                image = imutils.resize(image, width=camera.width_pixels)
            camera.cam_q.append(image)
            for detector in camera.detectors:
                self.run_detector(camera, image, detector)

    def run_detector(self, camera, image, detector):
        """ run detector on newest image and detector queue; perform detection

        For each detector, add most recently acquired image to detector queue.
        Apply detector critera to detector queue of images to evaluate events.
        Append messages about events detected, if any, to send_q queue. Also,
        append any images relevant to a detected event to send_q queue.

        Parameters:
            camera (Camera object): current camera
            image (openCV image): most recently acquired camera image
            detector (Detector object): current detector to apply to image
                queue (e.g. motion)
        """

        if detector.draw_roi:
            cv2.rectangle(image,
                          detector.top_left,
                          detector.bottom_right,
                          detector.draw_color,
                          detector.draw_line_width)
        # For troubleshooting purposes - print time on images
        if detector.draw_time:
            display_time = datetime.now().isoformat(sep=' ', timespec='microseconds')
            cv2.putText(image,
                        display_time,
                        detector.draw_time_org,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        detector.draw_time_fontScale,
                        detector.draw_time_color,
                        detector.draw_time_width,
                        cv2.LINE_AA)
        # detect state (light, etc.) and put images and events into send_q
        detector.detect_state(camera, image, self.send_q)

    def fix_comm_link(self):
        """ Evaluate, repair and restart communications link with hub.

        Perhaps in future: Close and restart imageZMQ if possible, else restart
        program or reboot computer.

        For now, just call a function that will cause imagenode.py to exit.
        """
        self.shutdown_imagenode()
        sys.exit()

    def shutdown_imagenode(self):
        """ Start a process that shuts down the imagenode.py program.

        It is very difficult to shutdown the imagenode.py program from
        within a thread since sys.exit() only exits the thread. And most other
        techniques that will end a program immediately don't close resources
        appropriately. But creating a subprocess that kills the imagenode.py
        parent process works cleanly. There really should be an easier way to
        end a Python program from a thread, but after lots of searching, this
        works. And, yes, it is messy. Please find a better one and send a
        pull request!

        """
        multiprocessing.Process(daemon=True,
                   args=((self.pid,)),
                   target=self.shutdown_process_by_pid).start()
        sys.exit()

    def shutdown_process_by_pid(self, pid):
        os.kill(pid, signal.SIGTERM)
        sys.exit()

    def process_hub_reply(self, hub_reply):
        """ Process hub reply if it is other than "OK".

        A hub reply is normally "OK", but could be "send 10 images" or
        "set resolution: (320, 240)". This method processes hub requests.
        This may involve sending a requested image sequence, changing a setting,
        or restarting the computer.
        """

        # Typical response from hub is "OK" if there are no user or
        #    automated librian requests. Almost all responses are just "OK"
        #    therefore the default process_hub_reply is "pass"
        # TODO Respond to hub repies if they are other than 'OK'
        # for example, push "send 10 frames" request onto deque
        #     and then add "do requested extra frames" to detectors loop
        #     so that images get sent even though there is no routine reason
        pass

    def closeall(self, settings):
        """ Close all resources, including cameras, lights, GPIO.

        Parameters:
            settings (Settings object): settings object created from YAML file
        """

        for camera in self.camlist:
            camera.cam.stop()
        for light in self.lights:
            light.turn_off()
        if settings.sensors or settings.lights:
            GPIO.cleanup()
        if self.health.stall_p:
            self.health.stall_p.terminate()
            self.health.stall_p.join()
        if settings.send_threading:
            self.send_q.stop_sending()
        self.sender.zmq_socket.setsockopt(zmq.LINGER, 0)  # prevents ZMQ hang on exit
        self.sender.close()