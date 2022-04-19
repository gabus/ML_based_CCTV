from cv2 import cv2


class VideoStream:
    def __init__(self, resolution=(640, 480), framerate=20):
        self.stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'X264'))
        self.stream.set(3, resolution[0])
        self.stream.set(4, resolution[1])
        self.stream.set(cv2.CAP_PROP_FPS, framerate)

        self.grabbed, self.frame = self.stream.read()

    def get_new_frame(self):
        # Return the most recent frame
        self.grabbed, self.frame = self.stream.read()
        return self.frame
