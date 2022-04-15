import os
from cv2 import cv2
import datetime
import settings
from loguru import logger
import functools


class Writer:
    location = ''

    def write_image(self, file_name: str, image):
        sub_dir = datetime.datetime.now().strftime("%Y-%m-%d")
        full_dir = os.path.join(settings.PHOTOS_LOCATION, sub_dir)

        if not os.path.exists(full_dir):
            os.mkdir(full_dir)

        file_path = os.path.join(full_dir, file_name)
        logger.debug("Write file")
        cv2.imwrite(file_path, image)

        # cache the location
        self.location = file_path
        self.get_last_location(file_name)

    @functools.lru_cache(maxsize=128, typed=False)
    def get_last_location(self, _id: str) -> str:
        logger.debug({'Fetching file location (not using cache)': _id})
        return self.location
