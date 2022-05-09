from time import time


class FPS:

    def __init__(self):
        self.last_frame_time = time()

    def get_frame_time(self) -> float:
        rs = time() - self.last_frame_time
        self.last_frame_time = time()
        return rs

    def update(self):
        self.last_frame_time = time()
