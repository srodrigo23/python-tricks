class SendQueue:
    """ Implements a send_q replacement that uses threaded sends

    The default send_q is a deque that is filled in a read_cameras forever loop
    in the imagenode.py main() event loop. When the default send_q tests True
    because it contains images to send, the send_frame loop empties the send_q.
    It works, but has speed issues when sending occurs while motion detection is
    actively occuring at the same time.

    This class creates a drop-in replacement for send_q. This replacement
    send_q will always return len(send_q) as 0 as if empty, so that the main()
    event loop will loop forever in node.read_cameras() without ever sending
    anything. This is implemented by providing _bool_ and __len__ methods to
    prevent read_cameras from ever reaching the send_frame portion of the main
    imagenode.py event loop.

    This send_q replacement append() method will operate in read_cameras just as
    the deque did, but has a send_messages_forever method in a separate
    thread to send (message, image tuples) to empty the send_q. This
    implementation of send_q allows the imagenode.py main program to remain
    unchanged when send_threading is not set to True in the yaml settings.

    Parameters:
        maxlen (int): maximum length of send_q deque
        send_frame (func): the ImageNode method that sends frames
        process_hub_reply (func): the ImageNode method that processes hub replies

    """
    def __init__(self, maxlen=500, send_frame=None, process_hub_reply=None):
        self.send_q = deque(maxlen=maxlen)
        self.send_frame = send_frame
        self.process_hub_reply = process_hub_reply
        self.keep_sending = True

    def __bool__(self):
        return False  # so that the read loop keeps reading forever

    def __len__(self):
        return 0  # so that the main() send loop is never entered

    def append(self, text_and_image):
        self.send_q.append(text_and_image)

    def send_messages_forever(self):
        # this will run in a separate thread
        # the "sleep()" calls allow main thread more time for image capture
        while self.keep_sending:
            if len(self.send_q) > 0:  # send until send_q is empty
                text, image = self.send_q.popleft()
                sleep(0.0000001)  # sleep before sending
                hub_reply = self.send_frame(text, image)
                self.process_hub_reply(hub_reply)
            else:
                sleep(0.0000001)  # sleep before checking send_q again

    def start(self):
        # start the thread to read frames from the video stream
        t = threading.Thread(target=self.send_messages_forever)
        t.daemon = True
        t.start()

    def stop_sending(self):
        self.keep_sending = False
        sleep(0.0000001)  # sleep to allow ZMQ to clear buffer
