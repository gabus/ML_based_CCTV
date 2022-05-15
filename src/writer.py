import os
from cv2 import cv2
import datetime
from settings import PHOTOS_STORAGE_LOCATION


class Writer:

    @staticmethod
    def write_image(image):
        file_name = "%s.jpeg" % (datetime.datetime.now().strftime("%Y-%m-%d_(%H-%M-%S)_%f"))
        sub_dir = datetime.datetime.now().strftime("%Y-%m-%d")
        full_dir = os.path.join(PHOTOS_STORAGE_LOCATION, sub_dir)

        if not os.path.exists(full_dir):
            os.mkdir(full_dir)

        file_path = os.path.join(full_dir, file_name)
        cv2.imwrite(file_path, image)

        return file_path
