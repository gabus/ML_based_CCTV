import os
from cv2 import cv2
import datetime


class Writer:
    def __init__(self):
        self.storage_location_root = 'photos'
        self.location = ''

    def write_image(self, image):
        file_name = "%s.jpeg" % (datetime.datetime.now().strftime("%Y-%m-%d_(%H-%M-%S)_%f"))
        sub_dir = datetime.datetime.now().strftime("%Y-%m-%d")
        full_dir = os.path.join(self.storage_location_root, sub_dir)

        if not os.path.exists(full_dir):
            os.mkdir(full_dir)

        file_path = os.path.join(full_dir, file_name)
        cv2.imwrite(file_path, image)

        return file_path
