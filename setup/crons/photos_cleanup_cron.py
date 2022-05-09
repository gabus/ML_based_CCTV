import os
import datetime
import shutil
import logging
from src.settings import STORAGE_RETENTION_DAYS


logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

path = "/home/pi/tflite/photos"
now = datetime.datetime.now()
day_diff = datetime.timedelta(days=STORAGE_RETENTION_DAYS)

yesterday = (now - day_diff).strftime("%Y-%m-%d")

joined = os.path.join(path, yesterday)

if os.path.isdir(joined):
    logging.info("Folder found to delete: " + joined)
    shutil.rmtree(joined)
else:
    logging.info("folder not found: " + joined)
