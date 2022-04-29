from cv2 import cv2
from loguru import logger
import time


class VideoStream:
    def __init__(self, _resolution, _frame_rate):
        self.resolution = _resolution
        self.frame_rate = _frame_rate

        self.camera_refresh_rate = 5  # how often camera resets brightness in minutes
        self.last_camera_refresh_time = time.time()

        # self.stream = cv2.VideoCapture(0)
        # self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'JPEG'))
        self.stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'X264'))

        # When you try to set random resolution, opencv sets nearest resolution if that resolution is not available.
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, _resolution[0])
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, _resolution[1])
        self.stream.set(cv2.CAP_PROP_FPS, _frame_rate)

        self.grabbed, self.frame = self.stream.read()

        logger.info({
                    "info": "Regardless user requested resolution, actual frame resolution is as following",
                    "width": self.stream.get(cv2.CAP_PROP_FRAME_WIDTH),
                    "height": self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    })

    def get_new_frame(self):
        """
        Return the most recent frame
        """
        self.grabbed, self.frame = self.stream.read()
        return self.frame

    def reset(self):
        logger.warning("Restarting VideoStream")
        st = time.time()
        self.stream.release()
        self.__init__(self.resolution, self.frame_rate)
        logger.warning("VideoStream successfully restarted in {} seconds".format(round(time.time() - st, 2)))
