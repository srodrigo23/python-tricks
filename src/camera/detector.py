class Detector:
    """ Methods and attributes of a detector for motion, light, etc.

    Each detector is setup with ROI tuples and various parameters.
    Detector options that are common to all detectors are set up here.
    Detector options that are specific to individual detector types (like
    'light', are set up in detector specific sections here).

    Parameters:
        detector (text): dict key for a specific detector for this camera
        detectors (dict): dictionary of all detectors for this camera
        nodename (str): nodename to identify event messages and images sent
        viewnane (str): viewname to identify event messages and images sent
    """

    def __init__(self, detector, detectors, nodename, viewname):
        """ Initializes all the detector using settings from the YAML file.
        """

        self.detector_type = detector
        # set detect_state function to detector_type (e.g., light or motion)
        if detector == 'light':
            self.detect_state = self.detect_light
            if 'threshold' in detectors[detector]:
                self.threshold = detectors[detector]['threshold']
            else:
                self.threshold = 100  # 100 is a default for testing
            if 'min_frames' in detectors[detector]:
                self.min_frames = detectors[detector]['min_frames']
            else:
                self.min_frames = 5  # 5 is default
            # need to remember min_frames of state history to calculate state
            self.state_history_q = deque(maxlen=self.min_frames)

        elif detector == 'motion':
            self.detect_state = self.detect_motion
            self.moving_frames = 0
            self.still_frames = 0
            self.total_frames = 0
            if 'delta_threshold' in detectors[detector]:
                self.delta_threshold = detectors[detector]['delta_threshold']
            else:
                self.delta_threshold = 5  # 5 is a default for testing
            if 'min_area' in detectors[detector]:
                self.min_area = detectors[detector]['min_area']
            else:
                self.min_area = 3  # 3 is default percent of ROI
            if 'min_motion_frames' in detectors[detector]:
                self.min_motion_frames = detectors[detector]['min_motion_frames']
            else:
                self.min_motion_frames = 3  # 3 is default
            if 'min_still_frames' in detectors[detector]:
                self.min_still_frames = detectors[detector]['min_still_frames']
            else:
                self.min_still_frames = 3  # 3 is default
            self.min_frames = max(self.min_motion_frames, self.min_still_frames)
            if 'blur_kernel_size' in detectors[detector]:
                self.blur_kernel_size = detectors[detector]['blur_kernel_size']
            else:
                self.blur_kernel_size = 15  # 15 is default blur_kernel_size
            if 'print_still_frames' in detectors[detector]:
                self.print_still_frames = detectors[detector]['print_still_frames']
            else:
                self.print_still_frames = True  # True is default print_still_frames

        if 'ROI' in detectors[detector]:
            self.roi_pct = literal_eval(detectors[detector]['ROI'])
        else:
            self.roi_pct = ((0, 0), (100, 100))
        if 'draw_roi' in detectors[detector]:
            self.draw_roi = literal_eval(detectors[detector]['draw_roi'])
            self.draw_color = self.draw_roi[0]
            self.draw_line_width = self.draw_roi[1]
        else:
            self.draw_roi = None
        # name of the ROI detector section
        if 'roi_name' in detectors[detector]:
            self.roi_name = detectors[detector]['roi_name']
        else:
            self.roi_name = ''
        # include ROI name in log events
        if 'log_roi_name' in detectors[detector]:
            self.log_roi_name = detectors[detector]['log_roi_name']
        else:
            self.log_roi_name = False
        # draw timestamp on image
        if 'draw_time' in detectors[detector]:
            self.draw_time = literal_eval(detectors[detector]['draw_time'])
            self.draw_time_color = self.draw_time[0]
            self.draw_time_width = self.draw_time[1]
            if 'draw_time_org' in detectors[detector]:
                self.draw_time_org = literal_eval(detectors[detector]['draw_time_org'])
            else:
                self.draw_time_org = (0, 0)
            if 'draw_time_fontScale' in detectors[detector]:
                self.draw_time_fontScale = detectors[detector]['draw_time_fontScale']
            else:
                self.draw_time_fontScale = 1
        else:
            self.draw_time = None
        send_frames = 'None Set'
        self.frame_count = 0
        # send_frames option can be 'continuous', 'detected event', 'none'
        if 'send_frames' in detectors[detector]:
            send_frames = detectors[detector]['send_frames']
            if not send_frames:  # None was specified; send 0 frames
                self.frame_count = 0
            if 'detect' in send_frames:
                self.frame_count = 10  # detected events default; adjusted later
            elif 'continuous' in send_frames:
                self.frame_count = -1  # send continuous flag
            elif 'none' in send_frames:  # don't send any frames
                self.frame_count = 0
        else:
            self.frame_count = -1  # send continuous flag
        # send_count option is an integer of how many frames to send if event
        if 'send_count' in detectors[detector]:
            self.send_count = detectors[detector]['send_count']
        else:
            self.send_count = 5  # default number of frames to send per event
        # send_test_images option: if True, send test images like ROI, Gray
        if 'send_test_images' in detectors[detector]:
            self.send_test_images = detectors[detector]['send_test_images']
        else:
            self.send_test_images = False  # default is NOT to send test images

        # self.event_text is the text message for this detector that is
        # sent when the detector state changes
        # example: JeffOffice Window|light|dark
        # example: JeffOffice Window|light|lighted
        # self.event_text will have self.current_state appended when events are sent
        node_and_view = ' '.join([nodename, viewname]).strip()
        self.event_text = '|'.join([node_and_view, self.detector_type])

        # An event is a change of state (e.g., 'dark' to 'lighted')
        # Every detector is instantiated with all states = 'unknown'
        self.current_state = 'unknown'
        self.last_state = 'unknown'

        self.msg_image = np.zeros((2, 2), dtype="uint8")  # blank image tiny
        if self.send_test_images:
            # set the blank image wide enough to hold message of send_test_images
            self.msg_image = np.zeros((5, 320), dtype="uint8")  # blank image wide

    def detect_state(self, camera, image, send_q):
        """ Placeholder function will be set to specific detection function

        For example, detect_state() will be set to detect_light() during
        detector.__init__()
        """
        print('Therefore, should never get to this print statement')
        pass

    def detect_light(self, camera, image, send_q):
        """ Detect if ROI is 'lighted' or 'dark'; send event message and images

        After adding current image to 'event state' history queue, detect if the
        ROI state has changed (e.g., has state changed to 'lighted' from 'dark'.)

        If the state has changed, send an event message and the event images.
        (However, if send_frames option is 'continuous', images have already
        been sent, so there is no need to send the event images.)

        If state has not changed, just store the image state into 'event state'
        history queue for later comparison and return.

        Parameters:
            camera (Camera object): current camera
            image (OpenCV image): current image
            send_q (Deque): where (text, image) tuples are appended to be sent
        """

        # if we are sending images continuously, append current image to send_q
        if self.frame_count == -1:  # -1 code to send all frames continuously
            text_and_image = (camera.text, image)
            send_q.append(text_and_image)

        # crop ROI & convert to grayscale
        x1, y1 = self.top_left
        x2, y2 = self.bottom_right
        ROI = image[y1:y2, x1:x2]
        gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        # calculate current_state of ROI
        gray_mean = int(np.mean(gray))
        if gray_mean > self.threshold:
            state = 'lighted'
            state_num = 1
        else:
            state = 'dark'
            state_num = -1
        if self.send_test_images:
            images = []
            images.append(('ROI', ROI,))
            images.append(('Grayscale', gray,))
            state_values = []
            state_values.append(('State', state,))
            state_values.append(('Mean Pixel Value', str(gray_mean),))
            self.send_test_data(images, state_values, send_q)
        self.state_history_q.append(state_num)
        if len(self.state_history_q) < self.min_frames:
            return  # not enough history to check for a state change

        # have enough history now, so...
        #   determine if there has been a change in state
        if self.state_history_q.count(-1) == self.min_frames:
            self.current_state = 'dark'
        elif self.state_history_q.count(1) == self.min_frames:
            self.current_state = 'lighted'
        else:
            return  # state has not stayed the same for self.min_frames
        if self.current_state == self.last_state:
            return  # there has been no state change and hence no event yet

        # state has changed from last reported state, therefore
        # send event message, reporting current_state, by appending it to send_q
        text = '|'.join([self.event_text, self.current_state])
        if self.log_roi_name:
            text = '|'.join([text, self.roi_name])
        text_and_image = (text, self.msg_image)
        send_q.append(text_and_image)

        # if frame_count = -1, then already sending images continuously...
        #   so no need to send the images of this detected event
        # if frame_count > 0, need to send send_count images from the cam_q
        #   by appending them to send_q
        if self.frame_count > 0:  # then need to send images of this event
            send_count = min(len(camera.cam_q), self.send_count)
            for i in range(-send_count, -1):
                text_and_image = (camera.text, camera.cam_q[i])
                send_q.append(text_and_image)

        # Now that current state has been sent, it becomes the last_state
        self.last_state = self.current_state

    def detect_motion(self, camera, image, send_q):
        """ Detect if ROI is 'moving' or 'still'; send event message and images

        After adding current image to 'event state' history queue, detect if the
        ROI state has changed (e.g., has state changed to 'moving' from 'still'.)

        If the state has changed, send an event message and the event images.
        (However, if send_frames option is 'continuous', images have already
        been sent, so there is no need to send the event images.)

        If state has not changed, just store the image into 'event state'
        history queue for later comparison and return.

        Parameters:
            camera (Camera object): current camera
            image (OpenCV image): current image
            send_q (Deque): where (text, image) tuples are appended to be sent

        This function borrowed a lot from a motion detector tutorial post by
        Adrian Rosebrock on PyImageSearch.com. See README.rst for details.
        """

        #####
        # Branch to fix duplicate frames; see GitHub issues #15 (&#12)
        #####

        # if we are sending images continuously, append current image to send_q
        if self.frame_count == -1:  # -1 code ==> send all frames continuously
            text_and_image = (camera.text, image)
            send_q.append(text_and_image)  # send current image

        # crop ROI & convert to grayscale & apply GaussianBlur
        x1, y1 = self.top_left
        x2, y2 = self.bottom_right
        ROI = image[y1:y2, x1:x2]
        gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray,
                                (self.blur_kernel_size, self.blur_kernel_size),
                                0)
        # If no history yet, save the first image as the  average image
        if self.total_frames < 1:
            self.average = gray.copy().astype('float')
        else:
            # add gray image to weighted average image
            cv2.accumulateWeighted(gray, self.average, 0.5)
        # frame delta is the absolute difference between gray and self.average
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.average))
        # threshold the frame delta image and dilate the thresholded image
        thresholded = cv2.threshold(frameDelta, self.delta_threshold,
                                    255, cv2.THRESH_BINARY)[1]
        thresholded = cv2.dilate(thresholded, None, iterations=2)
        # find contours in thresholded image
        # OpenCV version 3.x returns a 3 value tuple
        # OpenCV version 4.x returns a 2 value tuple
        contours_tuple = cv2.findContours(thresholded.copy(),
                                          cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)
        contours = contours_tuple[-2]  # captures contours value correctly for both versions of OpenCV
        state = 'still'
        area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self.min_area_pixels:
                continue
            state = 'moving'
        if state == 'moving':
            self.moving_frames += 1
        else:
            self.moving_frames = 0
            self.still_frames += 1
        # Optionally, send various test images to visually tune settings
        if self.send_test_images:  # send some intermediate test images
            images = []
            images.append(('ROI', ROI,))
            images.append(('Grayscale', gray,))
            images.append(('frameDelta', frameDelta,))
            images.append(('thresholded', thresholded,))
            state_values = []
            state_values.append(('State', self.current_state,))
            state_values.append(('N Contours', str(len(contours)),))
            state_values.append(('Area', str(area),))
            self.send_test_data(images, state_values, send_q)
        else:
            sleep(0.02)  # for testing
            pass

        self.total_frames += 1
        if self.total_frames < self.min_frames:
            return  # not enough history to check for a state change

        # have enough history now, so...
        #   determine if there has been a change in state
        if self.moving_frames >= self.min_motion_frames:
            self.current_state = 'moving'
            self.still_frames = 0
        elif self.still_frames >= self.min_still_frames:
            self.current_state = 'still'
        else:
            return  # not enought frames of either state; return for more
        if self.current_state == self.last_state:
            return  # there has been no state change and hence no event yet

        # state has changed from last reported state, so...
        # send event message reporting current_state by appending it to send_q
        text = '|'.join([self.event_text, self.current_state])
        if self.log_roi_name:
            text = '|'.join([text, self.roi_name])
        text_and_image = (text, self.msg_image)
        send_q.append(text_and_image)

        # if frame_count = -1, then already sending images continuously...
        #   so no need to send the images of this detected event
        # if frame_count > 0, need to send send_count images from the cam_q
        #   by appending them to send_q
        if self.frame_count > 0:  # then need to send images of this event
            send_count = min(len(camera.cam_q), self.send_count)
            if (self.current_state == 'still') and (self.print_still_frames is False):
                send_count = 0
            for i in range(-send_count, -1):
                text_and_image = (camera.text, camera.cam_q[i])
                send_q.append(text_and_image)

        # Now that current state has been sent, it becomes the last_state
        self.last_state = self.current_state

    def send_test_data(self, images, state_values, send_q):
        """ Sends various test data, images, computed state values via send_q

        Used for testing, this function takes a set of images and computed
        values such as number of contours, averge light intensity value,
        and computed state, such as "moving" and "still" and puts these values
        into small images that can be displayed in a simple test hub for
        tuning the settings parameters of a detector.

        Parameters:
            images (list): test images to send for display, e.g., ROI, grayscale
            state_values (list): the name and value of tuning parameters, such
                as state, area, N_contours, Mean Pixel Value, etc.
        """
        for text_and_image in images:
            send_q.append(text_and_image)
        font = cv2.FONT_HERSHEY_SIMPLEX
        for text_and_value in state_values:
            text, value = text_and_value
            state_image = np.zeros((50, 200), dtype="uint8")  # blank image
            cv2.putText(state_image, value, (10, 35), font,
                        1, (255, 255, 255), 2, cv2.LINE_AA)
            text_and_image = (text, state_image)
            send_q.append(text_and_image)
