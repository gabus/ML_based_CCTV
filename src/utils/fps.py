from time import time


class FPS:

    """
    doesn't work..
    """
    def __init__(self):
        self.start_time = time()
        self.frames = 1
        self.next_reset_timer = time() + 10 * 60

    def update(self):
        self.frames = self.frames + 1

    def get_fps(self) -> float:
        if self.next_reset_timer < time():
            self.reset()

        return self.frames / (time() - self.start_time)

    def reset(self):
        self.__init__()
